from src.null_trace import compare_shadows, load_csv


def test_compare_shadows_finds_diff():
    cur = load_csv("tests/data/current.csv")
    prev = load_csv("tests/data/previous_shadow.csv")
    out = compare_shadows(cur, prev)
    assert out["meta"]["diff_count"] >= 1
