import hashlib

import pytest

from src.data.cli import main
from src.data.inventory import build_inventory


def test_missing_dataset(tmp_path):
    with pytest.raises(ValueError, match="Dataset directory does not exist"):
        build_inventory(tmp_path / "missing")


def test_empty_dataset(tmp_path):
    assert build_inventory(tmp_path)["file_count"] == 0
    assert main(["inventory", "--dataset-path", str(tmp_path)]) == 1


def test_csv_metadata_and_hash(tmp_path):
    path = tmp_path / "traffic.CSV"
    path.write_text("frame.len,nhãn\n42,Bình thường\n", encoding="utf-8-sig")
    before = path.read_bytes()
    result = build_inventory(tmp_path, source="fixture", version="v1")
    entry = result["files"][0]
    assert result["csv_count"] == 1
    assert result["version"] == "v1"
    assert entry["size_bytes"] == len(before)
    assert entry["sha256"] == hashlib.sha256(before).hexdigest()
    assert entry["csv"]["encoding"] == "utf-8-sig"
    assert entry["csv"]["header"] == ["frame.len", "nhãn"]
    assert entry["csv"]["columns"][0]["group"] == "frame"
    assert path.read_bytes() == before


def test_schema_order_and_duplicate_files(tmp_path):
    for name in ("first.csv", "duplicate.csv"):
        (tmp_path / name).write_text("class,frame.len\nNormal,41\n")
    (tmp_path / "reordered.csv").write_text("frame.len,class\n41,Normal\n")
    result = build_inventory(tmp_path)
    assert len(result["schema_groups"]) == 2
    assert list(result["duplicate_files"].values()) == [["duplicate.csv", "first.csv"]]


def test_row_count_and_malformed_width(tmp_path):
    (tmp_path / "traffic.csv").write_text('x,y\n1,2\nwrong\n"a\nb",3\n4,5\n6,7\n8,9\n')
    report = build_inventory(tmp_path, chunk_size=2)["files"][0]["csv"]
    assert report["row_count"] == 5
    assert report["malformed_line_examples"] == [3]


@pytest.mark.parametrize("header", ["", "x,x\n1,2\n", "x, \n1,2\n"])
def test_bad_header(tmp_path, header):
    (tmp_path / "traffic.csv").write_text(header)
    report = build_inventory(tmp_path)["files"][0]["csv"]
    assert report["errors"]
    assert report["row_count"] == 0


def test_cli_rejects_output_inside_dataset(tmp_path):
    with pytest.raises(SystemExit) as error:
        main(["inventory", "--dataset-path", str(tmp_path), "--output", str(tmp_path / "out.json")])
    assert error.value.code == 2
