#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Dict, Any

EXPECTED_ROWS = 32768


def canon_dump(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Ingest B32K canonical lattice from CSV into b32k.json"
    )
    ap.add_argument("--csv", required=True, help="Path to B32K_canonical_alphabet_*.csv")
    ap.add_argument("--canon", default="b32k.json", help="Path to b32k.json")
    ap.add_argument("--set-generated-utc", action="store_true")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    canon_path = Path(args.canon)

    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")
    if not canon_path.exists():
        raise SystemExit(f"Canon not found: {canon_path}")

    rows = []
    anchors: Dict[str, Dict[str, str]] = {}

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = int(row["index"])
            plane = int(row["plane"])
            r = int(row["r"])
            c = int(row["c"])
            aid = row["anchor_domain"]
            label = row["anchor_label"]

            rows.append(
                {
                    "index": idx,
                    "hex": f"0x{row['hex']}",
                    "unicode_point": f"U+{row['unicode_point']}",
                    "plane": plane,
                    "r": r,
                    "c": c,
                    "anchor_id": aid,
                }
            )

            if aid not in anchors:
                domain = label.split("/", 1)[0] if "/" in label else label
                anchors[aid] = {
                    "domain": domain,
                    "label": label,
                }

    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(
            f"Expected {EXPECTED_ROWS} rows, got {len(rows)} — aborting"
        )

    doc = json.loads(canon_path.read_text(encoding="utf-8"))

    if args.set_generated_utc:
        doc.setdefault("meta", {})["generated_utc"] = int(time.time())

    doc["anchors"] = dict(sorted(anchors.items()))
    doc["alphabet"] = {
        "shape": {
            "lattice": "rxc",
            "fields": ["index", "hex", "unicode_point", "plane", "r", "c", "anchor_id"],
        },
        "rows": rows,
    }

    canon_path.write_text(canon_dump(doc), encoding="utf-8")

    print("OK")
    print(f"Rows ingested : {len(rows)}")
    print(f"Anchors built : {len(anchors)}")
    print(f"Wrote canon   : {canon_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
