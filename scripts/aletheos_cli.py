#!/usr/bin/env python3
"""
Aletheos CLI 001

Pre-ratification witness CLI.

Usage:
  python scripts/aletheos_cli.py ':'
  python scripts/aletheos_cli.py MARK "open the door"
  python scripts/aletheos_cli.py help

Boundary:
  This is a Python-hosted witness CLI.
  It is not self-hosting.
  It is not ratified.
  It does not assign B32K indices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "artifacts" / "json" / "aletheos_operator_registry_001.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def digest_obj(obj: Dict[str, Any]) -> str:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


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


def noop_receipt(token: str, registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    receipt = {
        "id": "aletheos_cli_noop_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": token
        },
        "operator": {
            "key": operator.get("key"),
            "token": operator.get("token"),
            "label": operator.get("label"),
            "family": operator.get("family"),
            "meaning": operator.get("meaning")
        },
        "semantics": {
            "claim_advanced": False,
            "positive_authority": False,
            "state_before": "NULL",
            "state_after": "NULL",
            "final_state": "NULL",
            "result": "accepted_noop",
            "receipt_kind": "lawful_stillness_receipt"
        },
        "boundary": {
            "python_hosted": True,
            "self_hosting": False,
            "ratified": False,
            "b32k_index_assigned_here": False,
            "commercial_reliance_allowed": False,
            "sovereign_reliance_allowed": False
        },
        "keeper": "The first lawful instruction is silence that succeeds."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt


def mark_receipt(token: str, payload_parts: List[str], registry: Dict[str, Any], operator: Dict[str, Any]) -> Dict[str, Any]:
    payload_text = " ".join(payload_parts).strip()
    payload = {
        "text": payload_text,
        "text_sha256": hashlib.sha256(payload_text.encode("utf-8")).hexdigest()
    }
    receipt = {
        "id": "aletheos_cli_mark_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": registry.get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": " ".join([token] + payload_parts).strip(),
            "payload": payload
        },
        "operator": {
            "key": operator.get("key"),
            "token": operator.get("token"),
            "label": operator.get("label"),
            "family": operator.get("family"),
            "meaning": operator.get("meaning")
        },
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
        "boundary": {
            "python_hosted": True,
            "self_hosting": False,
            "ratified": False,
            "b32k_index_assigned_here": False,
            "commercial_reliance_allowed": False,
            "sovereign_reliance_allowed": False,
            "admit_not_performed": True,
            "return_not_performed": True,
            "verify_not_performed": True
        },
        "keeper": "MARK proves the machine can notice without trusting."
    }
    receipt["receipt_sha256"] = digest_obj(receipt)
    return receipt


def error_receipt(token: str, reason: str, registry: Dict[str, Any] | None = None) -> Dict[str, Any]:
    receipt = {
        "id": "aletheos_cli_error_receipt_001",
        "artifact_kind": "cli_receipt",
        "status": "pre_ratification",
        "created_at": utc_now(),
        "lane": (registry or {}).get("lane", "b32k.aletheos.bound.v1"),
        "input": {
            "token": token,
            "raw_command": token
        },
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


def print_receipt_summary(receipt: Dict[str, Any]) -> None:
    sem = receipt.get("semantics", {})
    op = receipt.get("operator", {})
    print("Aletheos CLI receipt")
    print("token: " + str(op.get("token", receipt.get("input", {}).get("token", ""))))
    if op.get("key"):
        print("operator: " + str(op.get("key")))
    print("result: " + str(sem.get("result")))
    print("claim_advanced: " + str(sem.get("claim_advanced")).lower())
    if sem.get("admission"):
        print("admission: " + str(sem.get("admission")))
    print("state: " + str(sem.get("state_before")) + " -> " + str(sem.get("state_after")))
    print("receipt_sha256: " + receipt["receipt_sha256"])
    print("")
    print(json.dumps(receipt, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="aletheos_cli",
        description="Pre-ratification Aletheos witness CLI."
    )
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
        print("")
        print("Commands:")
        print("  :     NOOP, lawful stillness, no claim advanced")
        print("  MARK  mark a candidate trace, not yet admitted or trusted")
        print("  help  show this help")
        print("")
        print("Boundary:")
        print("  Python-hosted, pre-ratification, not self-hosting, not reliance-bearing.")
        return 0

    registry = load_registry()
    operator = find_operator_by_token(registry, parsed.command)

    if parsed.command == ":" and operator:
        receipt = noop_receipt(parsed.command, registry, operator)
        if parsed.json:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print_receipt_summary(receipt)
        return 0

    if parsed.command == "MARK" and operator:
        if not parsed.args:
            receipt = error_receipt(parsed.command, "mark_requires_payload", registry)
            print_receipt_summary(receipt)
            return 2
        receipt = mark_receipt(parsed.command, parsed.args, registry, operator)
        if parsed.json:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print_receipt_summary(receipt)
        return 0

    receipt = error_receipt(parsed.command, "unknown_or_unadmitted_operator", registry)
    print_receipt_summary(receipt)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
