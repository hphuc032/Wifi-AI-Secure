"""Profile CSVs with disk-backed counts and a bounded CSV batch size."""

import json
import math
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

from .inventory import dataset_files, read_csv
from .schemas import column_group, identifier_candidate


NUMERIC = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:e[+-]?[0-9]+)?", re.IGNORECASE)
MISSING = {"nan", "null", "na", "n/a", "<na>"}


def value_kind(value: str) -> str:
    if value == "":
        return "empty"
    stripped = value.strip()
    if not stripped:
        return "whitespace"
    if stripped.casefold() in MISSING:
        return "missing_token"
    if stripped.casefold().lstrip("+-") in {"inf", "infinity"}:
        return "nonfinite"
    if NUMERIC.fullmatch(stripped):
        return "numeric" if math.isfinite(float(stripped)) else "nonfinite"
    return "text"


def column_report(db, file_id, index, name, kinds, rows, is_label):
    missing = sum(kinds[key] for key in ("empty", "whitespace", "missing_token"))
    present = rows - missing
    distinct, mode = db.execute(
        "SELECT COUNT(*), COALESCE(MAX(n), 0) FROM cell WHERE file_id=? AND col=?",
        (file_id, index),
    ).fetchone()
    if not present:
        dtype = "missing"
    elif kinds["numeric"] or kinds["nonfinite"]:
        dtype = "mixed" if kinds["text"] else "numeric"
    else:
        dtype = "categorical" if distinct <= 50 else "string"
    result = {
        "name": name, "observed_dtype": dtype, "label_candidate": is_label,
        "identifier_candidate": identifier_candidate(name),
        "missing": missing, "missing_percent": 100 * missing / rows if rows else None,
        "nan_literal_count": kinds["nan_literal"],
        "value_kind_counts": dict(kinds), "distinct_nonmissing": distinct,
        "constant": distinct == 1, "near_constant": distinct > 1 and mode / present >= 0.99,
        "high_cardinality": distinct >= 50 and distinct / present >= 0.95,
        "numeric_conversion_failures": kinds["text"] + kinds["nonfinite"] if dtype in {"mixed", "numeric"} else None,
        "invalid_nonfinite": kinds["nonfinite"],
    }
    if is_label:
        result["class_frequency"] = dict(db.execute(
            "SELECT value, n FROM cell WHERE file_id=? AND col=? ORDER BY value", (file_id, index),
        ))
        result["largest_to_smallest_ratio"] = (
            mode / min(result["class_frequency"].values()) if distinct else None
        )
    return result


def profile_file(db, root, path, file_id, encoding, chunk_size, label_columns):
    kinds = defaultdict(Counter)
    indexes = None

    def accumulate(header, chunk):
        nonlocal indexes
        if indexes is None:
            indexes = sorted(range(len(header)), key=header.__getitem__)
        schema = json.dumps([header[index] for index in indexes], ensure_ascii=False)
        row_counts = Counter()
        cell_counts = Counter()
        for row in chunk:
            row_counts[json.dumps([row[index] for index in indexes], ensure_ascii=False)] += 1
            for index, value in enumerate(row):
                kind = value_kind(value)
                kinds[index][kind] += 1
                if value.strip().casefold() == "nan":
                    kinds[index]["nan_literal"] += 1
                if kind not in {"empty", "whitespace", "missing_token"}:
                    cell_counts[index, value] += 1
        with db:
            db.executemany(
                "INSERT INTO records VALUES (?, ?, ?, ?) "
                "ON CONFLICT(schema, value, file_id) DO UPDATE SET n=n+excluded.n",
                ((schema, row, file_id, count) for row, count in row_counts.items()),
            )
            db.executemany(
                "INSERT INTO cell VALUES (?, ?, ?, ?) "
                "ON CONFLICT(file_id, col, value) DO UPDATE SET n=n+excluded.n",
                ((file_id, col, value, count) for (col, value), count in cell_counts.items()),
            )

    report = read_csv(path, encoding=encoding, chunk_size=chunk_size, on_chunk=accumulate)
    rows = report["row_count"]
    report["path"] = path.relative_to(root).as_posix()
    report["columns"] = [
        column_report(db, file_id, index, name, kinds[index], rows,
                      name in label_columns or column_group(name) == "label_candidate")
        for index, name in enumerate(report["header"])
    ]
    report["duplicate_rows"] = db.execute(
        "SELECT COALESCE(SUM(n-1),0) FROM records WHERE file_id=?", (file_id,),
    ).fetchone()[0]
    report["duplicate_percent"] = 100 * report["duplicate_rows"] / rows if rows else None
    report["absent_requested_labels"] = sorted(set(label_columns) - set(report["header"]))
    report["profile_complete"] = not (report["errors"] or report["malformed_rows"])
    return report


def build_profile(root: Path, *, encoding: str | None = None, chunk_size: int = 4096,
                  label_columns: tuple[str, ...] = (), source: str | None = None,
                  version: str | None = None, scratch_dir: Path | None = None) -> dict:
    started = perf_counter()
    files = [path for path in dataset_files(root) if path.suffix.lower() == ".csv"]
    reports = []
    observed_types = defaultdict(lambda: defaultdict(list))
    label_totals = defaultdict(Counter)
    missing_labels = Counter()
    with TemporaryDirectory(prefix="awid3-profile-", dir=scratch_dir) as temp:
        db = sqlite3.connect(Path(temp) / "counts.sqlite3")
        try:
            db.executescript("""
                CREATE TABLE records (
                    schema TEXT, value TEXT, file_id INTEGER, n INTEGER,
                    PRIMARY KEY (schema, value, file_id)
                ) WITHOUT ROWID;
                CREATE INDEX records_by_file ON records (file_id);
                CREATE TABLE cell (
                    file_id INTEGER, col INTEGER, value TEXT, n INTEGER,
                    PRIMARY KEY (file_id, col, value)
                ) WITHOUT ROWID;
            """)
            for file_id, path in enumerate(files):
                report = profile_file(db, root, path, file_id, encoding, chunk_size, label_columns)
                reports.append(report)
                for column in report["columns"]:
                    observed_types[column["name"]][column["observed_dtype"]].append(report["path"])
                    if column["label_candidate"]:
                        label_totals[column["name"]].update(column["class_frequency"])
                        missing_labels[column["name"]] += column["missing"]
                with db:
                    db.execute("DELETE FROM cell WHERE file_id=?", (file_id,))
            for file_id, report in enumerate(reports):
                report["rows_shared_with_other_files"] = db.execute("""
                    SELECT COALESCE(SUM(current.n), 0) FROM records AS current
                    WHERE current.file_id=? AND EXISTS (
                        SELECT 1 FROM records AS other WHERE other.schema=current.schema
                        AND other.value=current.value AND other.file_id<>current.file_id
                    )
                """, (file_id,)).fetchone()[0]
        finally:
            db.close()
    return {
        "source": source, "version": version, "csv_count": len(files), "files": reports,
        "inconsistent_types": {name: dict(types) for name, types in observed_types.items()
                               if len(types) > 1},
        "label_totals": {
            name: {"class_frequency": dict(counts), "missing": missing_labels[name],
                   "largest_to_smallest_ratio": max(counts.values()) / min(counts.values())
                   if counts else None}
            for name, counts in label_totals.items()
        },
        "elapsed_seconds": perf_counter() - started,
    }
