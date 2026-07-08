#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
json_dir = root / "artifacts" / "json"
errors = []

def bad(msg):
    errors.append(msg)
    print("BAD " + msg)

objs = {}
for path in sorted(json_dir.glob("*.json")):
    rel = str(path.relative_to(root))
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        objs[rel] = obj
        print("OK " + rel)
    except Exception as exc:
        bad(f"{rel} json parse failed: {exc}")

for rel, obj in objs.items():
    if isinstance(obj, dict) and not obj.get("id"):
        bad(f"{rel} missing id")

reg = objs.get("artifacts/json/structural_key_registry_001.json")
if reg:
    keys = [x.get("key") for x in reg.get("keys", [])]
    if len(keys) != len(set(keys)):
        bad("structural key registry has duplicate keys")

gen = objs.get("artifacts/json/kjv_genesis_1_structural_concordance_001.json")
if gen and reg:
    ids = [x.get("id") for x in gen.get("entries", [])]
    if len(ids) != len(set(ids)):
        bad("genesis 1 artifact has duplicate entry ids")
    allowed = {x.get("key") for x in reg.get("keys", [])}
    for e in gen.get("entries", []):
        if e.get("structural_key") not in allowed:
            bad(f"unknown structural key in genesis 1: {e.get('structural_key')}")

if errors:
    print(f"validation=fail error_count={len(errors)}")
    sys.exit(1)
print("validation=pass")
