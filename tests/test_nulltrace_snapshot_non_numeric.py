from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    header = list(rows[0].keys())
    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(r.get(h, "") for h in header))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_snapshot_diff_ignores_non_numeric_cells(tmp_path: Path) -> None:
    prev_csv = tmp_path / "previous_shadow.csv"
    cur_csv = tmp_path / "current.csv"

    _write_csv(prev_csv, [{"a": "1", "label": "x"}, {"a": "2", "label": "y"}])
    _write_csv(cur_csv, [{"a": "3", "label": "x"}, {"a": "2", "label": "z"}])

    prev_out = tmp_path / "prev_out"
    cur_out = tmp_path / "cur_out"

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "nulltrace",
            "snapshot",
            str(prev_csv),
            "--output-dir",
            str(prev_out),
        ]
    )
    prev_manifest = list((prev_out / "shadows").glob("*/manifest.json"))[0]

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "nulltrace",
            "snapshot",
            str(cur_csv),
            "--previous-shadow",
            str(prev_manifest),
            "--output-dir",
            str(cur_out),
        ]
    )

    diff_path = list((cur_out / "shadows").glob("*/shadow_diff.json"))[0]
    diff = json.loads(diff_path.read_text(encoding="utf-8"))
    column_changes = diff["diff"]["column_changes"]

    assert "label" not in column_changes
    assert "a" in column_changes
