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

def ok(msg):
    print("OK " + msg)

objs = {}
for path in sorted(json_dir.glob("*.json")):
    rel = str(path.relative_to(root))
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        objs[rel] = obj
        ok(rel)
    except Exception as exc:
        bad(f"{rel} json parse failed: {exc}")

for rel, obj in objs.items():
    if isinstance(obj, dict) and not obj.get("id"):
        bad(f"{rel} missing id")

reg = objs.get("artifacts/json/structural_key_registry_001.json")
allowed = set()
index_by_key = {}
if reg:
    keys = [x.get("key") for x in reg.get("keys", [])]
    if len(keys) != len(set(keys)):
        bad("structural key registry has duplicate keys")
    for row in reg.get("keys", []):
        key = row.get("key")
        idx = row.get("b32k_symbol_index")
        if not key:
            bad("structural key registry row missing key")
            continue
        allowed.add(key)
        if not isinstance(idx, int) or idx < 0 or idx > 32767:
            bad(f"structural key {key} has invalid b32k_symbol_index {idx}")
        else:
            index_by_key[key] = idx
else:
    bad("missing structural key registry")

for rel, obj in objs.items():
    if not isinstance(obj, dict):
        continue
    if obj.get("translation") == "King James Version" and "entries" in obj:
        entries = obj.get("entries", [])
        ids = [x.get("id") for x in entries]
        if len(ids) != len(set(ids)):
            bad(f"{rel} has duplicate entry ids")
        for e in entries:
            eid = e.get("id", "<missing>")
            key = e.get("structural_key")
            if key not in allowed:
                bad(f"{rel} {eid} unknown structural_key {key}")
                continue
            idx = e.get("b32k_symbol_index")
            if idx != index_by_key.get(key):
                bad(f"{rel} {eid} index mismatch for {key}: entry={idx} registry={index_by_key.get(key)}")
            if e.get("b32k_binding_status") != "bound_to_structural_key_registry_001":
                bad(f"{rel} {eid} missing binding status")
            for req in ["source", "source_phrase", "keeper_line", "boundary_note"]:
                if not e.get(req):
                    bad(f"{rel} {eid} missing {req}")

if errors:
    print(f"validation=fail error_count={len(errors)}")
    sys.exit(1)

print("validation=pass")
