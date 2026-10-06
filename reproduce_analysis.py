"""Reproduce aggregate CSV tables from one institutional XLSX; no network/AI calls."""
import argparse
import json
from pathlib import Path
from analysis import run_checks, new_output_dir, write_tables, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--figures", action="store_true", help="Also export Figures 1 and 2 as 600 dpi JPEG")
    args = parser.parse_args()
    try:
        tables, report = run_checks(args.input)
        if args.figures:
            from make_figures import render_figures
        new_output_dir(args.output_dir)
        write_tables(args.output_dir, tables)
        write_json(args.output_dir / "validation_report.json", report)
        if args.figures:
            render_figures(tables, args.output_dir)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"Reproduction failed: {exc}\n")
    print(json.dumps({"output_dir": str(args.output_dir), "counts": report["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
