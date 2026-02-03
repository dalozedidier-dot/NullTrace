from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(prog="tools.validate_soak")
    parser.add_argument("--overview", type=str, required=True)
    args = parser.parse_args()

    overview_path = Path(args.overview)
    if not overview_path.exists():
        raise FileNotFoundError(str(overview_path))

    data = json.loads(overview_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("overview.json must be a JSON object")

    if data.get("schema") != "nulltrace.soak.overview.v1":
        raise ValueError("unexpected schema")

    runs = data.get("runs")
    if not isinstance(runs, int) or runs < 0:
        raise ValueError("runs must be a non-negative integer")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("artifacts must be an object")

    if artifacts.get("run_files_glob") != "run_*.json":
        raise ValueError("run_files_glob must be 'run_*.json'")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
