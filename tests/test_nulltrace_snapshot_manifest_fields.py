from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(r))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_snapshot_manifest_has_required_fields(tmp_path: Path) -> None:
    csv_path = tmp_path / "input.csv"
    _write_csv(csv_path, ["x", "y"], [["1", "10"], ["2", "20"], ["3", "30"]])

    out_dir = tmp_path / "out"
    subprocess.check_call(
        [sys.executable, "-m", "nulltrace", "snapshot", str(csv_path), "--output-dir", str(out_dir)]
    )

    manifests = list((out_dir / "shadows").glob("*/manifest.json"))
    assert manifests, "manifest.json not created"
    manifest = json.loads(manifests[0].read_text(encoding="utf-8"))

    assert manifest["schema"] == "nulltrace.shadow.manifest.v1"
    assert "created_at_utc" in manifest
    assert manifest["source_csv"].endswith("input.csv")
    assert isinstance(manifest["source_csv_sha256"], str) and len(manifest["source_csv_sha256"]) == 64
    assert manifest["n_rows"] == 3
    assert manifest["columns"] == ["x", "y"]
