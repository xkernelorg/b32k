#!/usr/bin/env python3
"""
Aletheos CLI 001

Pre-ratification witness CLI.

Usage:
  python scripts/aletheos_cli.py ':'
  python scripts/aletheos_cli.py MARK "open the door"
  python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
  python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json
  python scripts/aletheos_cli.py RETURN ~/tmp/admit.json --json > ~/tmp/return.json
  python scripts/aletheos_cli.py RECEIPT ~/tmp/return.json
  python scripts/aletheos_cli.py help

Boundary:
  Python-hosted witness CLI.
  Not self-hosting.
  Not ratified.
  Does not assign B32K indices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "artifacts" / "json" / "aletheos_operator_registry_001.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def digest_obj(obj: Dict[str, Any]) -> str:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def digest_without_receipt_sha(obj: Dict[str, Any]) -> str:
    copy = dict(obj)
    copy.pop("receipt_sha256", None)
    return digest_obj(copy)


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise SystemExit(f"missing operator registry: {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def find_operator_by_token(registry: Dict[str, Any], token: str) -> Dict[str, Any] | None:
    for fam in registry.get("operator_families", []):
        for op in fam.get("operators", []):
            if op.get("token") == token:
                out = dict(op)
                out["family"] = fam.get("family")
                out["family_role"] = fam.get("role")
                return out
    return None


def base_boundary() -> Dict[str, Any]:
    return {
        "python_hosted": True,
        "self_hosting": False,
        "ratified": False,
        "b32k_index_assigned_here": False,
        "commercial_reliance_allowed": False,
        "sovereign_reliance_allowed": False
    }


def operator_view(operator: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "key": operator.get("key"),
        "token": operator.get("token"),
        "label": operator.get("label"),
        "family": operator.get("family"),
        "meaning": operator.get("meaning")
    }


def error_receipt(token: str, reason: str, registry: Dict[str, Any] | None = None) -> Dict[str, Any]:
    receipt = {
        "id": "aletheos_cli_error_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": (registry or {}).get("lane", "b32k.aletheos.bound.v1"),
        "input": {"token": token, "raw_command": token},
        "semantics": {
            "claim_advanced": False,
            "positive_authority": False,
            "state_before": "NULL",
            "state_after": "REJECTED",
            "final_state": "REJECTED",
            "result": "rejected",
            "reason": reason
        },
        "boundary": {
            "python_hosted": True,
            "self_hosting": False,
            "ratified": False,
            "b32k_index_assigned_here": False
        }
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt


def noop_receipt(token: str, registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    receipt = {
        "id": "aletheos_cli_noop_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {"token": token, "raw_command": token},
        "operator": operator_view(operator),
        "semantics": {
            "claim_advanced": False,
            "positive_authority": False,
            "state_before": "NULL",
            "state_after": "NULL",
            "final_state": "NULL",
            "result": "accepted_noop",
            "receipt_kind": "lawful_stillness_receipt"
        },
        "boundary": base_boundary(),
        "keeper": "The first lawful instruction is silence that succeeds."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt


def mark_receipt(token: str, payload_parts: List[str], registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    payload_text = " ".join(payload_parts).strip()
    boundary = base_boundary()
    boundary.update({"admit_not_performed": True, "return_not_performed": True, "verify_not_performed": True})
    receipt = {
        "id": "aletheos_cli_mark_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": " ".join([token] + payload_parts).strip(),
            "payload": {
                "text": payload_text,
                "text_sha256": hashlib.sha256(payload_text.encode("utf-8")).hexdigest()
            }
        },
        "operator": operator_view(operator),
        "semantics": {
            "claim_advanced": True,
            "positive_authority": False,
            "state_before": "NULL",
            "state_after": "MARKED",
            "final_state": "MARKED",
            "result": "marked",
            "admission": "not_yet_admitted",
            "receipt_kind": "candidate_trace_receipt",
            "trust_bearing": False,
            "reliance_allowed": False
        },
        "boundary": boundary,
        "keeper": "MARK proves the machine can notice without trusting."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt


def validate_receipt(obj: Dict[str, Any], expected_id: str, expected_result: str, expected_final: str) -> Tuple[bool, str]:
    if obj.get("id") != expected_id:
        return False, "input_is_not_" + expected_id
    sem = obj.get("semantics", {})
    if sem.get("result") != expected_result or sem.get("final_state") != expected_final:
        return False, "receipt_state_or_result_mismatch"
    given = obj.get("receipt_sha256")
    expected = digest_without_receipt_sha(obj)
    if not given or given != expected:
        return False, "receipt_hash_mismatch"
    return True, "ok"


def admit_receipt(token: str, mark_path: Path, registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    try:
        mark_obj = json.loads(mark_path.read_text(encoding="utf-8"))
    except Exception:
        return error_receipt(token, "admit_requires_readable_mark_receipt_json", registry)

    ok, reason = validate_receipt(mark_obj, "aletheos_cli_mark_receipt_001", "marked", "MARKED")
    if not ok:
        return error_receipt(token, reason, registry)
    if mark_obj.get("semantics", {}).get("admission") != "not_yet_admitted":
        return error_receipt(token, "mark_receipt_already_admitted_or_malformed", registry)

    boundary = base_boundary()
    boundary.update({
        "mark_receipt_required": True,
        "mark_receipt_hash_verified": True,
        "return_not_performed": True,
        "verify_not_performed": True,
        "reliance_allowed": False
    })
    receipt = {
        "id": "aletheos_cli_admit_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": f"{token} {mark_path}",
            "mark_receipt_path": str(mark_path),
            "mark_receipt_sha256": mark_obj.get("receipt_sha256"),
            "marked_payload": mark_obj.get("input", {}).get("payload", {})
        },
        "operator": operator_view(operator),
        "semantics": {
            "claim_advanced": True,
            "positive_authority": False,
            "state_before": "MARKED",
            "state_after": "ADMITTED",
            "final_state": "ADMITTED",
            "result": "admitted",
            "receipt_kind": "admission_receipt",
            "trust_bearing": False,
            "reliance_allowed": False,
            "admission": "admitted_to_witness_passage",
            "admitted_operator_path": "MARK -> ADMIT"
        },
        "boundary": boundary,
        "keeper": "ADMIT opens the passage without pretending the return has happened."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt


def return_receipt(token: str, admit_path: Path, registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    try:
        admit_obj = json.loads(admit_path.read_text(encoding="utf-8"))
    except Exception:
        return error_receipt(token, "return_requires_readable_admit_receipt_json", registry)

    ok, reason = validate_receipt(admit_obj, "aletheos_cli_admit_receipt_001", "admitted", "ADMITTED")
    if not ok:
        return error_receipt(token, reason, registry)

    boundary = base_boundary()
    boundary.update({
        "admit_receipt_required": True,
        "admit_receipt_hash_verified": True,
        "receipt_not_performed": True,
        "verify_not_performed": True,
        "reliance_allowed": False
    })
    receipt = {
        "id": "aletheos_cli_return_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": f"{token} {admit_path}",
            "admit_receipt_path": str(admit_path),
            "admit_receipt_sha256": admit_obj.get("receipt_sha256"),
            "mark_receipt_sha256": admit_obj.get("input", {}).get("mark_receipt_sha256"),
            "marked_payload": admit_obj.get("input", {}).get("marked_payload", {})
        },
        "operator": operator_view(operator),
        "semantics": {
            "claim_advanced": True,
            "positive_authority": False,
            "state_before": "ADMITTED",
            "state_after": "RETURNED",
            "final_state": "RETURNED",
            "result": "returned",
            "receipt_kind": "return_receipt",
            "trust_bearing": False,
            "reliance_allowed": False,
            "return": "returned_from_witness_passage",
            "admitted_operator_path": "MARK -> ADMIT -> RETURN"
        },
        "boundary": boundary,
        "keeper": "RETURN brings the trace home without pretending trust has been granted."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt



def receipt_receipt(token: str, return_path: Path, registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return_obj = json.loads(return_path.read_text(encoding="utf-8"))
    except Exception:
        return error_receipt(token, "receipt_requires_readable_return_receipt_json", registry)

    ok, reason = validate_receipt(return_obj, "aletheos_cli_return_receipt_001", "returned", "RETURNED")
    if not ok:
        return error_receipt(token, reason, registry)

    boundary = base_boundary()
    boundary.update({
        "return_receipt_required": True,
        "return_receipt_hash_verified": True,
        "verify_not_performed": True,
        "reliance_allowed": False
    })
    receipt = {
        "id": "aletheos_cli_receipt_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": f"{token} {return_path}",
            "return_receipt_path": str(return_path),
            "return_receipt_sha256": return_obj.get("receipt_sha256"),
            "admit_receipt_sha256": return_obj.get("input", {}).get("admit_receipt_sha256"),
            "mark_receipt_sha256": return_obj.get("input", {}).get("mark_receipt_sha256"),
            "marked_payload": return_obj.get("input", {}).get("marked_payload", {})
        },
        "operator": operator_view(operator),
        "semantics": {
            "claim_advanced": True,
            "positive_authority": False,
            "state_before": "RETURNED",
            "state_after": "RECEIPTED",
            "final_state": "RECEIPTED",
            "result": "receipted",
            "receipt_kind": "returned_trace_ledger_receipt",
            "trust_bearing": False,
            "reliance_allowed": False,
            "receipt": "returned_trace_recorded",
            "admitted_operator_path": "MARK -> ADMIT -> RETURN -> RECEIPT"
        },
        "boundary": boundary,
        "keeper": "RECEIPT gives the returned trace a body without pretending verification is complete."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt

def print_receipt_summary(receipt: Dict[str, Any]) -> None:
    sem = receipt.get("semantics", {})
    op = receipt.get("operator", {})
    inp = receipt.get("input", {})
    print("Aletheos CLI receipt")
    print("token: " + str(op.get("token", inp.get("token", ""))))
    if op.get("key"):
        print("operator: " + str(op.get("key")))
    print("result: " + str(sem.get("result")))
    if sem.get("reason"):
        print("reason: " + str(sem.get("reason")))
    print("claim_advanced: " + str(sem.get("claim_advanced")).lower())
    if sem.get("admission"):
        print("admission: " + str(sem.get("admission")))
    if sem.get("return"):
        print("return: " + str(sem.get("return")))
    print("state: " + str(sem.get("state_before")) + " -> " + str(sem.get("state_after")))
    print("receipt_sha256: " + receipt["receipt_sha256"])
    print("")
    print(json.dumps(receipt, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(prog="aletheos_cli", description="Pre-ratification Aletheos witness CLI.")
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("args", nargs="*")
    parser.add_argument("--json", action="store_true", help="emit compact JSON only")
    parsed = parser.parse_args()

    if parsed.command in ("help", "-h", "--help"):
        print("Aletheos CLI 001")
        print("")
        print("Usage:")
        print("  python scripts/aletheos_cli.py ':'")
        print("  python scripts/aletheos_cli.py MARK \"open the door\"")
        print("  python scripts/aletheos_cli.py MARK \"open the door\" --json > ~/tmp/mark.json")
        print("  python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json")
        print("  python scripts/aletheos_cli.py RETURN ~/tmp/admit.json --json > ~/tmp/return.json")
        print("  python scripts/aletheos_cli.py RECEIPT ~/tmp/return.json")
        print("")
        print("Commands:")
        print("  :       NOOP, lawful stillness, no claim advanced")
        print("  MARK    mark a candidate trace, not yet admitted or trusted")
        print("  ADMIT   admit a valid MARK receipt into witness passage")
        print("  RETURN   return a valid ADMIT receipt from witness passage")
        print("  RECEIPT  record a valid RETURN receipt as returned trace body")
        print("  help     show this help")
        print("")
        print("Boundary:")
        print("  Python-hosted, pre-ratification, not self-hosting, not reliance-bearing.")
        return 0

    registry = load_registry()
    operator = find_operator_by_token(registry, parsed.command)

    if parsed.command == ":" and operator:
        receipt = noop_receipt(parsed.command, registry, operator)
        print(json.dumps(receipt, sort_keys=True, separators=(",", ":")) if parsed.json else "", end="")
        if not parsed.json:
            print_receipt_summary(receipt)
        return 0

    if parsed.command == "MARK" and operator:
        if not parsed.args:
            receipt = error_receipt(parsed.command, "mark_requires_payload", registry)
            print_receipt_summary(receipt)
            return 2
        receipt = mark_receipt(parsed.command, parsed.args, registry, operator)
        print(json.dumps(receipt, sort_keys=True, separators=(",", ":")) if parsed.json else "", end="")
        if not parsed.json:
            print_receipt_summary(receipt)
        return 0

    if parsed.command == "ADMIT" and operator:
        if len(parsed.args) != 1:
            receipt = error_receipt(parsed.command, "admit_requires_one_mark_receipt_file", registry)
            print_receipt_summary(receipt)
            return 2
        receipt = admit_receipt(parsed.command, Path(parsed.args[0]).expanduser(), registry, operator)
        ok = receipt.get("semantics", {}).get("result") == "admitted"
        if parsed.json and ok:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print_receipt_summary(receipt)
        return 0 if ok else 2

    if parsed.command == "RETURN" and operator:
        if len(parsed.args) != 1:
            receipt = error_receipt(parsed.command, "return_requires_one_admit_receipt_file", registry)
            print_receipt_summary(receipt)
            return 2
        receipt = return_receipt(parsed.command, Path(parsed.args[0]).expanduser(), registry, operator)
        ok = receipt.get("semantics", {}).get("result") == "returned"
        if parsed.json and ok:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print_receipt_summary(receipt)
        return 0 if ok else 2


    if parsed.command == "RECEIPT" and operator:
        if len(parsed.args) != 1:
            receipt = error_receipt(parsed.command, "receipt_requires_one_return_receipt_file", registry)
            print_receipt_summary(receipt)
            return 2
        receipt = receipt_receipt(parsed.command, Path(parsed.args[0]).expanduser(), registry, operator)
        ok = receipt.get("semantics", {}).get("result") == "receipted"
        if parsed.json and ok:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print_receipt_summary(receipt)
        return 0 if ok else 2

    receipt = error_receipt(parsed.command, "unknown_or_unadmitted_operator", registry)
    print_receipt_summary(receipt)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
