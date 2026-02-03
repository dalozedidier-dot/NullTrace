from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(prog="tools.nulltrace_soak")
    parser.add_argument("--runs", type=int, default=25)
    parser.add_argument("--constraints", type=str, required=False)
    parser.add_argument("--out-dir", type=str, required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    constraints_text = ""
    constraints_path = None
    if args.constraints:
        constraints_path = Path(args.constraints)
        if constraints_path.exists():
            constraints_text = constraints_path.read_text(encoding="utf-8")
        else:
            # Keep deterministic behavior: treat missing constraints as empty.
            constraints_text = ""

    # Deterministic placeholder artifacts.
    # Per-run marker files (small JSON) + a single overview.json.
    runs_written: list[dict[str, object]] = []
    for i in range(1, max(args.runs, 0) + 1):
        run_obj = {
            "run_index": i,
            "status": "ok",
        }
        (out_dir / f"run_{i:04d}.json").write_text(
            json.dumps(run_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        runs_written.append(run_obj)

    overview = {
        "schema": "nulltrace.soak.overview.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "runs": args.runs,
        "constraints_path": str(constraints_path) if constraints_path else None,
        "constraints_sha256": _sha256_text(constraints_text),
        "artifacts": {
            "run_files_glob": "run_*.json",
        },
    }

    (out_dir / "overview.json").write_text(
        json.dumps(overview, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "soak_done.txt").write_text(f"runs={args.runs}\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
