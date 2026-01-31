from pathlib import Path

from nulltrace.null_trace import snapshot, compare


def test_compare_shadows_finds_diff(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    prev_csv = repo_root / "tests" / "data" / "previous_shadow.csv"
    curr_csv = repo_root / "tests" / "data" / "current.csv"

    out_dir = tmp_path / "nulltrace_out"
    prev_res = snapshot(csv_path=prev_csv, output_dir=out_dir)
    curr_res = snapshot(csv_path=curr_csv, output_dir=out_dir)

    diff_obj = compare(Path(prev_res["shadow_dir"]), Path(curr_res["shadow_dir"]))

    d = diff_obj["diff"]
    assert (d["row_count_delta"] != 0) or d["added_columns"] or d["removed_columns"] or d["dtype_changes"] or d["column_changes"]
