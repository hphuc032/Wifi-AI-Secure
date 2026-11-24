import pytest

from src.data.profiling import build_profile


def profile(tmp_path, text, **options):
    (tmp_path / "test.csv").write_text(text, encoding="utf-8")
    return next(report for report in build_profile(tmp_path, **options)["files"]
                if report["path"] == "test.csv")


def test_missing_and_constant_columns(tmp_path):
    report = profile(tmp_path, "x,y\n,a\n   ,a\nNaN,a\n3,a\n", chunk_size=2)
    column = report["columns"][0]
    assert column["missing"] == 3
    assert column["missing_percent"] == 75
    assert column["nan_literal_count"] == 1
    assert column["value_kind_counts"]["whitespace"] == 1
    assert report["columns"][1]["constant"]


def test_duplicate_rows_across_chunks_and_reordered_files(tmp_path):
    (tmp_path / "other.csv").write_text("y,x\nb,3\n", encoding="utf-8")
    report = profile(tmp_path, "x,y\n3,b\n4,c\n3,b\n3,b\n", chunk_size=1)
    assert report["rows_shared_with_other_files"] == 3
    assert report["duplicate_rows"] == 2
    assert report["row_count"] == 4


def test_mixed_numeric_categorical_and_no_label(tmp_path):
    report = profile(tmp_path, "frame.len,protocol\n3,http\noops,dns\nInf,http\n")
    numeric, category = report["columns"]
    assert numeric["observed_dtype"] == "mixed"
    assert numeric["numeric_conversion_failures"] == 2
    assert numeric["invalid_nonfinite"] == 1
    assert category["observed_dtype"] == "categorical"
    assert not any(col["label_candidate"] for col in report["columns"])


def test_label_frequency_unicode_and_override(tmp_path):
    report = profile(tmp_path, "outcome,attack_type\nBình thường,Normal\nKhác,Khác\nKhác,\n",
                     label_columns=("outcome", "missing"))
    first, second = report["columns"]
    assert first["class_frequency"] == {"Bình thường": 1, "Khác": 2}
    assert first["largest_to_smallest_ratio"] == 2
    assert second["class_frequency"] == {"Normal": 1, "Khác": 1}
    assert second["missing"] == 1
    assert report["absent_requested_labels"] == ["missing"]


def test_schema_type_conflict(tmp_path):
    (tmp_path / "a.csv").write_text("x\n1\n", encoding="utf-8")
    (tmp_path / "b.csv").write_text("x\nabc\n", encoding="utf-8")
    assert build_profile(tmp_path)["inconsistent_types"] == {
        "x": {"numeric": ["a.csv"], "categorical": ["b.csv"]},
    }


def test_aggregate_label_totals(tmp_path):
    (tmp_path / "a.csv").write_text("x,target\n1,A\n2,A\n", encoding="utf-8")
    (tmp_path / "b.csv").write_text("target,x\nB,3\n,4\n", encoding="utf-8")
    (tmp_path / "c.csv").write_text("x\n5\n", encoding="utf-8")
    assert build_profile(tmp_path)["label_totals"]["target"] == {
        "class_frequency": {"A": 2, "B": 1}, "missing": 1, "largest_to_smallest_ratio": 2,
    }


def test_bad_csv_keeps_partial_chunk(tmp_path):
    report = profile(tmp_path, 'x,y\n3,a\n"unterminated\n', chunk_size=5)
    assert report["row_count"] == 1
    assert report["columns"][0]["distinct_nonmissing"] == 1
    assert report["errors"]
    assert not report["profile_complete"]


@pytest.mark.parametrize("chunk_size", [1, 2, 3, 100])
def test_counts_independent_of_chunk_size(tmp_path, chunk_size):
    report = profile(tmp_path, "class,x\nA,1\nB,2\nA,1\nA,1\nB,3\n", chunk_size=chunk_size)
    assert report["row_count"] == 5
    assert report["duplicate_rows"] == 2
    assert report["columns"][0]["class_frequency"] == {"A": 3, "B": 2}
