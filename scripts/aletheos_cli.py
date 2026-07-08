#!/usr/bin/env python3
"""
Aletheos CLI 001

Pre-ratification witness CLI.

Usage:
  python scripts/aletheos_cli.py ':'
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
from typing import Any, Dict


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


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="aletheos_cli",
        description="Pre-ratification Aletheos witness CLI."
    )
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("--json", action="store_true", help="emit compact JSON only")
    args = parser.parse_args()

    if args.command in ("help", "-h", "--help"):
        print("Aletheos CLI 001")
        print("")
        print("Usage:")
        print("  python scripts/aletheos_cli.py ':'")
        print("")
        print("Commands:")
        print("  :     NOOP, lawful stillness, no claim advanced")
        print("  help  show this help")
        print("")
        print("Boundary:")
        print("  Python-hosted, pre-ratification, not self-hosting, not reliance-bearing.")
        return 0

    registry = load_registry()
    operator = find_operator_by_token(registry, args.command)

    if args.command == ":" and operator:
        receipt = noop_receipt(args.command, registry, operator)
        if args.json:
            print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        else:
            print("Aletheos CLI receipt")
            print("token: :")
            print("operator: OP_NOOP")
            print("result: accepted_noop")
            print("claim_advanced: false")
            print("state: NULL -> NULL")
            print("receipt_sha256: " + receipt["receipt_sha256"])
            print("")
            print(json.dumps(receipt, indent=2, sort_keys=True))
        return 0

    receipt = error_receipt(args.command, "unknown_or_unadmitted_operator", registry)
    print("Aletheos CLI receipt")
    print(f"token: {args.command}")
    print("result: rejected")
    print("reason: unknown_or_unadmitted_operator")
    print("receipt_sha256: " + receipt["receipt_sha256"])
    print("")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
