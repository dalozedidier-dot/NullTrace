from pathlib import Path

from nulltrace.null_trace import snapshot


def test_nulltrace_snapshot_and_diff(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    prev_csv = repo_root / "data" / "previous_shadow.csv"
    curr_csv = repo_root / "data" / "current.csv"
    out_dir = tmp_path / "nulltrace_out"

    prev_res = snapshot(csv_path=prev_csv, output_dir=out_dir)
    prev_shadow = Path(prev_res["shadow_dir"])

    curr_res = snapshot(csv_path=curr_csv, output_dir=out_dir, previous_shadow=prev_shadow)

    assert "diff" in curr_res
    shadow_dir = Path(curr_res["shadow_dir"])
    assert (shadow_dir / "manifest.json").exists()
    assert (shadow_dir / "shadow_profile.json").exists()
    assert (shadow_dir / "shadow_diff.json").exists()

    diff_obj = curr_res["diff"]
    assert diff_obj["diff"]["shape_change"]["after"][0] >= diff_obj["diff"]["shape_change"]["before"][0]
