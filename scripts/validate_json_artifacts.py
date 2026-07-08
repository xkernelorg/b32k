#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
bad = []

for path in sorted((root / "artifacts" / "json").glob("*.json")):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        print(f"OK {path.relative_to(root)}")
    except Exception as exc:
        bad.append((path, exc))
        print(f"BAD {path.relative_to(root)} :: {exc}")

if bad:
    raise SystemExit(1)

print("json_artifact_validation=pass")
