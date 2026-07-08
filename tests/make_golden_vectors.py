#!/usr/bin/env python3
"""
Generate golden test vectors for the canonical B32K codec.

This script is intentionally self-rooting so it can be executed directly:
    python spec/b32k/tests/make_golden_vectors.py

Golden vectors are written alongside the test suite and are used
to lock codec behavior across refactors.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import hashlib

# ---------------------------------------------------------------------
# Ensure repo root is on sys.path
# File lives at: repo/spec/b32k/tests/make_golden_vectors.py
# parents[3] == repo root
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from spec.b32k.codec import load_b32k_alphabet, encode  # noqa: E402


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
OUT_FILE = Path(__file__).with_name("golden_vectors.json")
ALPHABET_PATH = ROOT / "spec" / "b32k" / "b32k.json"


# ---------------------------------------------------------------------
# Test vectors
# ---------------------------------------------------------------------
VECTORS: dict[str, bytes] = {
    "empty": b"",
    "zero": b"\x00",
    "one": b"\x01",
    "zeros_4": b"\x00\x00\x00\x00",
    "inc_256": bytes(range(256)),
    "sha256_hello": hashlib.sha256(b"hello").digest(),
    "sha256_hello_world": hashlib.sha256(b"hello world").digest(),
}


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main() -> None:
    symbols, _ = load_b32k_alphabet(ALPHABET_PATH)

    golden: dict[str, dict[str, str]] = {}

    for name, raw in VECTORS.items():
        enc = encode(raw, symbols)
        golden[name] = {
            "hex": raw.hex(),
            "b32k": enc,
        }

    OUT_FILE.write_text(
        json.dumps(
            {
                "alphabet": "B32K canonical",
                "bits_per_symbol": 15,
                "vectors": golden,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {len(golden)} golden vectors → {OUT_FILE}")


if __name__ == "__main__":
    main()
