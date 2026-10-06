"""Check frozen-record consistency and compare recorded versus recounted aggregates."""
import argparse
import json
from pathlib import Path
from analysis import run_checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        _, report = run_checks(args.input)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"Validation failed: {exc}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
