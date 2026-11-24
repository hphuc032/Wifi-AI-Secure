# Data pipeline — Hoàng Phúc

Implement AWID3 inventory, loading, validation, cleaning, preprocessing and reproducible splitting here. See [interface contract](../../docs/INTERFACE_CONTRACT.md) and [work plan](../../docs/WORK_PLAN.md).

Do not commit raw AWID3 files. Add tests under `tests/data/` and document verified label/feature names.

From the repository root, run `python -m src.data.cli inventory --help` or
`python -m src.data.cli profile --help`. The CLI uses Python 3.11+ with no
runtime dependencies. Install pytest in a development environment for tests.
Output JSON goes to stdout by default. `--output` creates a new file outside
the input directory. Exit status 1 indicates at least one read/row issue or
no CSVs. Exit status 2 indicates invalid arguments or an input/output error.

See the [inventory](../../docs/data/DATA_INVENTORY.md) and
[quality report](../../docs/data/DATA_QUALITY_REPORT.md) for usage and verification status.
