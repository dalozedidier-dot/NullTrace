from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_nulltrace_soak_generates_overview_and_runs(tmp_path: Path) -> None:
    out_dir = tmp_path / "mass"
    cmd = [
        sys.executable,
        "-m",
        "tools.nulltrace_soak",
        "--runs",
        "3",
        "--out-dir",
        str(out_dir),
    ]
    subprocess.check_call(cmd)

    overview_path = out_dir / "overview.json"
    assert overview_path.exists()

    overview = json.loads(overview_path.read_text(encoding="utf-8"))
    assert overview["schema"] == "nulltrace.soak.overview.v1"
    assert overview["runs"] == 3

    # Expect per-run files.
    for i in range(1, 4):
        assert (out_dir / f"run_{i:04d}.json").exists()

    # Validate via validator module.
    vcmd = [
        sys.executable,
        "-m",
        "tools.validate_soak",
        "--overview",
        str(overview_path),
    ]
    subprocess.check_call(vcmd)
