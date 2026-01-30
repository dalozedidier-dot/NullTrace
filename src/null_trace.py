import argparse
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nulltrace")


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def save_shadow(df: pd.DataFrame, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    tmp = out_path + ".tmp"
    df.to_csv(tmp, index=False, lineterminator="\n")
    os.replace(tmp, out_path)


def _jsonable(x: Any) -> Any:
    try:
        if pd.isna(x):
            return None
    except Exception:
        pass
    if hasattr(x, "item"):
        try:
            return x.item()
        except Exception:
            pass
    return x


def compare_shadows(current: pd.DataFrame, previous: pd.DataFrame) -> Dict[str, Any]:
    diffs: List[Dict[str, Any]] = []
    cols = [c for c in current.columns if c in previous.columns]
    cur = current[cols].copy()
    prev = previous[cols].copy()

    n = min(len(cur), len(prev))
    for i in range(n):
        for c in cols:
            a = cur.iloc[i][c]
            b = prev.iloc[i][c]
            if (pd.isna(a) and pd.isna(b)) or (a == b):
                continue
            diffs.append({"row": int(i), "column": c, "current": _jsonable(a), "previous": _jsonable(b)})

    return {
        "meta": {
            "rows_current": int(len(current)),
            "rows_previous": int(len(previous)),
            "cols_compared": cols,
            "diff_count": int(len(diffs)),
        },
        "diffs": diffs,
    }


def write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


def main() -> int:
    ap = argparse.ArgumentParser(description="NullTrace: descriptive shadow diff")
    ap.add_argument("current_csv", help="Current CSV")
    ap.add_argument("--previous-shadow", required=False, help="Previous shadow CSV")
    ap.add_argument("--output-dir", default="outputs")
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    cur_df = load_csv(args.current_csv)
    shadow_path = os.path.join(args.output_dir, "current_shadow.csv")
    save_shadow(cur_df, shadow_path)

    report: Dict[str, Any] = {
        "tool": "NullTrace",
        "version": "0.1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "input": {"current": args.current_csv, "previous_shadow": args.previous_shadow},
        "artifacts": {"current_shadow": "current_shadow.csv"},
        "diff": None,
        "errors": {"errors": [], "warnings": []},
    }

    if args.previous_shadow:
        prev_df = load_csv(args.previous_shadow)
        report["diff"] = compare_shadows(cur_df, prev_df)

    out_report = os.path.join(args.output_dir, "shadow_report.json")
    write_json(out_report, report)
    logger.info("Wrote %s", out_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
