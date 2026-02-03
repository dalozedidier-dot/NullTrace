from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return ([], [])
        rows = [dict(r) for r in reader]
        return (list(reader.fieldnames), rows)


def _to_float(x: str) -> float | None:
    try:
        if x is None:
            return None
        s = str(x).strip()
        if s == "":
            return None
        return float(s)
    except Exception:
        return None


def _snapshot(csv_path: Path, output_dir: Path, previous_shadow_manifest: Path | None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    shadows_dir = output_dir / "shadows"
    shadows_dir.mkdir(parents=True, exist_ok=True)

    # Unique but simple: timestamp-based directory name.
    shadow_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    shadow_dir = shadows_dir / shadow_id
    shadow_dir.mkdir(parents=True, exist_ok=True)

    header, rows = _read_csv_rows(csv_path)
    csv_sha256 = _sha256_file(csv_path)

    manifest: dict[str, Any] = {
        "schema": "nulltrace.shadow.manifest.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_csv": str(csv_path),
        "source_csv_sha256": csv_sha256,
        "n_rows": len(rows),
        "columns": header,
    }

    (shadow_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if previous_shadow_manifest is not None:
        prev_manifest_obj = json.loads(previous_shadow_manifest.read_text(encoding="utf-8"))
        prev_shadow_dir = Path(previous_shadow_manifest).parent
        prev_csv_path = Path(prev_manifest_obj.get("source_csv", ""))

        # If prev source csv path is not available on this machine, fall back to the previous csv that exists in datasets.
        # BareFlux passes previous_shadow.csv and current.csv, so prev_csv_path should exist, but we keep it robust.
        if not prev_csv_path.exists():
            prev_csv_path = csv_path  # safe fallback: produce zero deltas

        prev_header, prev_rows = _read_csv_rows(prev_csv_path)

        common_cols = [c for c in header if c in prev_header]
        column_changes: dict[str, Any] = {}

        max_rows = min(len(rows), len(prev_rows))
        for col in common_cols:
            deltas: dict[str, float] = {}
            for i in range(max_rows):
                a = _to_float(prev_rows[i].get(col, ""))
                b = _to_float(rows[i].get(col, ""))
                if a is None or b is None:
                    continue
                deltas[str(i)] = float(b - a)
            if deltas:
                column_changes[col] = {"deltas": deltas}

        diff_obj: dict[str, Any] = {
            "schema": "nulltrace.shadow.diff.v1",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "previous_manifest": str(previous_shadow_manifest),
            "current_manifest": str(shadow_dir / "manifest.json"),
            "diff": {"column_changes": column_changes},
        }

        (shadow_dir / "shadow_diff.json").write_text(
            json.dumps(diff_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return shadow_dir


def main() -> int:
    parser = argparse.ArgumentParser(prog="nulltrace")
    sub = parser.add_subparsers(dest="cmd", required=True)

    snap = sub.add_parser("snapshot", help="Create a shadow snapshot (and diff if previous is provided).")
    snap.add_argument("csv", type=str, help="Path to CSV input")
    snap.add_argument("--output-dir", type=str, required=True, help="Directory where shadows/ will be written")
    snap.add_argument("--previous-shadow", type=str, required=False, help="Path to previous manifest.json")

    args = parser.parse_args()
    if args.cmd == "snapshot":
        csv_path = Path(args.csv)
        out_dir = Path(args.output_dir)
        prev = Path(args.previous_shadow) if getattr(args, "previous_shadow", None) else None
        _snapshot(csv_path, out_dir, prev)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
