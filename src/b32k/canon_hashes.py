#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict


ZERO64 = "0" * 64


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon_json_bytes(obj: Any) -> bytes:
    """
    Deterministic JSON bytes:
      - sort keys
      - no extra whitespace
      - UTF-8
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, doc: Dict[str, Any]) -> None:
    path.write_text(json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute and freeze B32K canon hashes deterministically.")
    ap.add_argument("--canon", default="b32k.json", help="Path to b32k.json")
    ap.add_argument("--delta", default="b32k.delta.jsonl", help="Path to b32k.delta.jsonl")
    ap.add_argument("--utc", type=int, default=0, help="generated_utc to set (0 = keep existing, -1 = now)")
    args = ap.parse_args()

    canon_path = Path(args.canon)
    delta_path = Path(args.delta)

    doc = load_json(canon_path)

    # Basic shape expectations
    if "anchors" not in doc or "alphabet" not in doc or "hashes" not in doc:
        raise SystemExit("b32k.json missing required top-level keys: anchors/alphabet/hashes")

    # Ensure hashes fields exist
    hashes = doc.setdefault("hashes", {})
    hashes.setdefault("canon_hash_algo", "SHA-256")
    hashes.setdefault("alphabet_hash", ZERO64)
    hashes.setdefault("anchors_hash", ZERO64)
    hashes.setdefault("full_hash", ZERO64)

    # Update generated_utc if requested
    if args.utc == -1:
        doc.setdefault("meta", {})["generated_utc"] = int(time.time())
    elif args.utc > 0:
        doc.setdefault("meta", {})["generated_utc"] = int(args.utc)

    # 1) Component hashes
    anchors_hash = sha256_hex(canon_json_bytes(doc["anchors"]))
    alphabet_hash = sha256_hex(canon_json_bytes(doc["alphabet"]))

    # 2) Full hash:
    #    - set component hashes
    #    - set full_hash to ZERO64 during computation to avoid circularity
    doc2 = json.loads(canon_json_bytes(doc).decode("utf-8"))  # deep copy via deterministic serialization
    doc2["hashes"]["anchors_hash"] = anchors_hash
    doc2["hashes"]["alphabet_hash"] = alphabet_hash
    doc2["hashes"]["full_hash"] = ZERO64
    full_hash = sha256_hex(canon_json_bytes(doc2))

    # Write hashes back into original doc
    doc["hashes"]["anchors_hash"] = anchors_hash
    doc["hashes"]["alphabet_hash"] = alphabet_hash
    doc["hashes"]["full_hash"] = full_hash

    save_json(canon_path, doc)

    # Append freeze record to delta log (JSONL)
    event = {
        "event": "freeze_hashes",
        "schema": doc.get("meta", {}).get("schema", "b32k.canon"),
        "schema_version": doc.get("meta", {}).get("schema_version", ""),
        "epoch": doc.get("meta", {}).get("epoch", ""),
        "generated_utc": doc.get("meta", {}).get("generated_utc", 0),
        "anchors_hash": anchors_hash,
        "alphabet_hash": alphabet_hash,
        "full_hash": full_hash,
    }
    delta_path.parent.mkdir(parents=True, exist_ok=True)
    with delta_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")

    print("OK")
    print(f"anchors_hash : {anchors_hash}")
    print(f"alphabet_hash: {alphabet_hash}")
    print(f"full_hash    : {full_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
