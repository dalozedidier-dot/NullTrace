from pathlib import Path
import os
import subprocess
import sys
import json


def _run(cmd, env):
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + "\n" + r.stderr
    return r


def test_cli_snapshot_smoke(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = tmp_path / "cli_out"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    # 1) Snapshot "avant" pour obtenir un shadow_dir
    cmd_prev = [
        sys.executable, "-m", "nulltrace", "snapshot",
        str(repo_root / "data" / "previous_shadow.csv"),
        "--output-dir", str(out_dir),
    ]
    r_prev = _run(cmd_prev, env)

    prev_obj = json.loads(r_prev.stdout.strip() or "{}")
    prev_shadow_dir = prev_obj.get("shadow_dir")
    assert prev_shadow_dir, r_prev.stdout

    # 2) Snapshot "après" avec previous-shadow pointant vers le shadow_dir
    cmd_curr = [
        sys.executable, "-m", "nulltrace", "snapshot",
        str(repo_root / "data" / "current.csv"),
        "--previous-shadow", prev_shadow_dir,
        "--output-dir", str(out_dir),
    ]
    _run(cmd_curr, env)

    shadows_dir = out_dir / "shadows"
    assert shadows_dir.exists()
    assert any(p.is_dir() for p in shadows_dir.iterdir())
