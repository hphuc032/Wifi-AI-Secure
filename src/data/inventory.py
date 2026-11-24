"""Build a JSON-compatible manifest without loading entire CSVs into memory."""

import codecs
import csv
import hashlib
from collections import defaultdict
from pathlib import Path
from time import perf_counter

from .schemas import column_group


DEFAULT_PATH = Path("data/raw/awid3")


def dataset_files(root: Path) -> list[Path]:
    if not root.is_dir():
        raise ValueError(f"Dataset directory does not exist or is not a directory: {root}")
    return sorted(path for path in root.rglob("*") if path.is_file() and not path.is_symlink())


def csv_encoding(path: Path, encoding: str | None) -> str:
    if encoding:
        return codecs.lookup(encoding).name
    with path.open("rb") as stream:
        prefix = stream.read(4)
    if prefix.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        return "utf-32"
    if prefix.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return "utf-16"
    return "utf-8-sig" if prefix.startswith(codecs.BOM_UTF8) else "utf-8"


def read_csv(path: Path, *, encoding: str | None = None, chunk_size: int = 4096,
             on_chunk=None) -> dict:
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    report = {"encoding": None, "header": [], "column_count": 0, "row_count": 0,
              "malformed_rows": 0, "malformed_line_examples": [], "errors": []}
    reader = None
    started = perf_counter()
    try:
        report["encoding"] = csv_encoding(path, encoding)
        with path.open(encoding=report["encoding"], newline="") as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader, [])
            report.update(header=header, column_count=len(header))
            if not header or any(not name.strip() for name in header) or len(set(header)) != len(header):
                report["errors"].append("Missing, blank or duplicate CSV header columns")
            else:
                chunk = []
                try:
                    for row in reader:
                        if len(row) == len(header):
                            report["row_count"] += 1
                            if on_chunk is not None:
                                chunk.append(row)
                                if len(chunk) == chunk_size:
                                    batch, chunk = chunk, []
                                    on_chunk(header, batch)
                        else:
                            report["malformed_rows"] += 1
                            if len(report["malformed_line_examples"]) < 10:
                                report["malformed_line_examples"].append(reader.line_num)

                finally:
                    if chunk:
                        on_chunk(header, chunk)
    except (OSError, UnicodeError, csv.Error, LookupError) as error:
        line = f" near line {reader.line_num}" if reader is not None else ""
        report["errors"].append(f"{type(error).__name__}{line}: {error}")
    report["elapsed_seconds"] = perf_counter() - started
    return report


def build_inventory(root: Path, *, encoding: str | None = None,
                    chunk_size: int = 4096, source: str | None = None,
                    version: str | None = None) -> dict:
    started = perf_counter()
    files = []
    checksums = defaultdict(list)
    schemas = defaultdict(list)
    for path in dataset_files(root):
        relative = path.relative_to(root).as_posix()
        entry = {"path": relative, "name": path.name,
                 "directory": path.relative_to(root).parent.as_posix(),
                 "format": path.suffix.lower().lstrip("."), "errors": []}
        try:
            entry["size_bytes"] = path.stat().st_size
            with path.open("rb") as stream:
                entry["sha256"] = hashlib.file_digest(stream, "sha256").hexdigest()
            checksums[entry["sha256"]].append(relative)
        except OSError as error:
            entry["errors"].append(str(error))
        if entry["format"] == "csv":
            report = read_csv(path, encoding=encoding, chunk_size=chunk_size)
            report["columns"] = [
                {"name": name, "group": column_group(name)} for name in report["header"]
            ]
            if report["header"]:
                schemas[tuple(report["header"])].append(relative)
            entry["csv"] = report
        files.append(entry)
    return {
        "source": source, "version": version, "file_count": len(files),
        "csv_count": sum("csv" in entry for entry in files), "files": files,
        "duplicate_files": {digest: paths for digest, paths in checksums.items() if len(paths) > 1},
        "schema_groups": [{"header": list(header), "paths": paths} for header, paths in schemas.items()],
        "elapsed_seconds": perf_counter() - started,
    }
