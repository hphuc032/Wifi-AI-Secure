"""Run dataset inspection from the repository root."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .inventory import DEFAULT_PATH, build_inventory
from .profiling import build_profile


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inventory", "profile"))
    parser.add_argument("--dataset-path", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--chunk-size", type=int, default=4096)
    parser.add_argument("--encoding")
    parser.add_argument("--source")
    parser.add_argument("--version")
    parser.add_argument("--label-column", action="append", default=[])
    parser.add_argument("--scratch-dir", type=Path)
    parser.add_argument("--output", type=Path, help="New JSON file. Defaults to standard output.")
    args = parser.parse_args(argv)
    if args.chunk_size < 1:
        parser.error("--chunk-size must be positive")
    if args.command == "inventory" and (args.label_column or args.scratch_dir):
        parser.error("--label-column and --scratch-dir only apply to profile")
    if args.output and args.output.resolve().is_relative_to(args.dataset_path.resolve()):
        parser.error("--output must be outside the source dataset folder")
    if args.scratch_dir and args.scratch_dir.resolve().is_relative_to(args.dataset_path.resolve()):
        parser.error("--scratch-dir must be outside the source dataset folder")
    options = dict(encoding=args.encoding, chunk_size=args.chunk_size,
                   source=args.source, version=args.version)
    try:
        if args.command == "inventory":
            result = build_inventory(args.dataset_path, **options)
        else:
            result = build_profile(args.dataset_path, label_columns=tuple(args.label_column),
                                   scratch_dir=args.scratch_dir, **options)
        if args.output:
            with args.output.open("x", encoding="utf-8") as stream:
                json.dump(result, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        else:
            print(json.dumps(result, indent=2))
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")
    if not result["csv_count"]:
        print("No CSV files found in the dataset directory.", file=sys.stderr)
        return 1
    issues = any(entry.get("errors") or entry.get("malformed_rows")
                 or entry.get("csv", {}).get("errors") or entry.get("csv", {}).get("malformed_rows")
                 for entry in result["files"])
    return int(issues)


if __name__ == "__main__":
    raise SystemExit(main())
