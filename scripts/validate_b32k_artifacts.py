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

canon = objs.get("artifacts/json/b32k_aletheos_canonical_index_001.json")
if canon:
    entries = canon.get("entries", [])
    seen = set()
    for e in entries:
        lane = e.get("lane")
        idx = e.get("index")
        key = (lane, idx)
        if key in seen:
            bad(f"canonical index duplicate lane/index: {lane} {idx}")
        seen.add(key)
        if not isinstance(idx, int) or idx < 0 or idx > 32767:
            bad(f"canonical index invalid index: {idx}")
        if idx == 0 and e.get("positive_authority") is not False:
            bad("index 0 must not carry positive authority")
    null_rows = [e for e in entries if e.get("index") == 0 and e.get("lane") == "b32k.aletheos.bound.v1"]
    root_rows = [e for e in entries if e.get("index") == 1 and e.get("lane") == "b32k.aletheos.bound.v1"]
    if not null_rows or null_rows[0].get("key") != "NULL_WELL":
        bad("missing NULL_WELL at b32k.aletheos.bound.v1 index 0")
    if not root_rows or root_rows[0].get("key") != "ALETHEOS_ROOT":
        bad("missing ALETHEOS_ROOT at b32k.aletheos.bound.v1 index 1")
else:
    bad("missing Aletheos canonical index")

op = objs.get("artifacts/json/aletheos_operator_profile_001.json")
if op:
    if op.get("primary_receipt_law") != "Q = M M^T":
        bad("operator profile primary receipt law mismatch")
    ops = op.get("operators", {})
    for key in ["A", "M", "M_transpose", "Q"]:
        if key not in ops:
            bad(f"operator profile missing operator {key}")

instr = objs.get("artifacts/json/aletheos_instruction_grammar_001.json")
if instr:
    ops = [x.get("opcode") for x in instr.get("instructions", [])]
    required = ["NOOP", "MARK", "ADMIT", "RETURN", "RECEIPT", "REJECT", "BIND", "VERIFY"]
    for x in required:
        if x not in ops:
            bad(f"instruction grammar missing {x}")
    if instr.get("failure_instruction") != "REJECT":
        bad("instruction grammar failure_instruction must be REJECT")
    if instr.get("rules", {}).get("no_q_no_trust") is not True:
        bad("instruction grammar must assert no_q_no_trust")

state = objs.get("artifacts/json/aletheos_execution_state_model_001.json")
if state:
    states = [x.get("state") for x in state.get("states", [])]
    required_states = ["NULL", "MARKED", "ADMITTED", "RETURNED", "RECEIPTED", "BOUND", "VERIFIED", "REJECTED", "REVOKED"]
    for x in required_states:
        if x not in states:
            bad(f"execution state model missing {x}")
    if state.get("positive_reliance_state") != "VERIFIED":
        bad("positive reliance state must be VERIFIED")
    if state.get("rules", {}).get("no_q_no_trust") is not True:
        bad("execution state model must assert no_q_no_trust")

apparatus = objs.get("artifacts/json/aletheos_minimal_apparatus_001.json")
if apparatus:
    order = apparatus.get("apparatus_order", [])
    required_order = ["null_well", "boundary", "state", "logic", "language", "sequence", "memory", "input_output", "receipt", "body"]
    if order != required_order:
        bad("minimal apparatus order mismatch")
    if apparatus.get("boundary", {}).get("apparatus_order_is_b32k_index_assignment") is not False:
        bad("minimal apparatus must not treat apparatus order as B32K index assignment")

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
        elif idx == 0:
            bad(f"structural key {key} illegally uses index 0")
        else:
            index_by_key[key] = idx
else:
    bad("missing structural key registry")

for rel, obj in objs.items():
    if not isinstance(obj, dict):
        continue
    if obj.get("translation") == "King James Version" and "entries" in obj:
        status = obj.get("status", "")
        require_binding = "bound" in status or "complete" in status
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
            if require_binding:
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
