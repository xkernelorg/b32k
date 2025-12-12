# spec/b32k/codec.py
# Canonical Base32768 (B32K) codec
# One symbol = 15 bits
#
# Canonical transport symbol (ASCII) is the INDEX token: "~00000" .. "~32767"
# This keeps the codec numeric + deterministic, while leaving anchor/plane/r/c
# as presentation metadata in b32k.json.
#
# IMPORTANT (length safety):
# Base32768 is not byte-aligned. To make decoding lossless for all byte strings
# (including leading 0x00 bytes), this codec prefixes the payload with a
# 4-byte big-endian length before packing into 15-bit groups.
# CAL-32K — B32K Canonical Action Lattice
-------------------------------------
# This module implements the canonical bijection defining the
# B32K Canonical Action Lattice (𝒜₃₂ₖ).
# One symbol = 15 bits of action.
# Odering, reversibility, and alignment are invariant.
# Behavior is locked by golden vectors.

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Tuple

BITS_PER_SYMBOL = 15
SYMBOL_CHARS = 6  # "~" + 5 digits
SYMBOL_MASK = (1 << BITS_PER_SYMBOL) - 1  # 0x7FFF


# ---------------------------------------------------------------------
# Alphabet loading (canonical)
# ---------------------------------------------------------------------

def load_b32k_alphabet(path: str | Path) -> Tuple[List[str], Dict[str, int]]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    rows = sorted(spec["alphabet"]["rows"], key=lambda r: r["index"])

    # CANONICAL SYMBOL = INDEX, not anchor_id
    symbols = [f"~{row['index']:05d}" for row in rows]

    if len(symbols) != 32768:
        raise ValueError(f"B32K alphabet must have 32768 symbols, got {len(symbols)}")
    if len(set(symbols)) != 32768:
        raise ValueError("B32K alphabet symbols must be unique")

    index = {sym: i for i, sym in enumerate(symbols)}
    return symbols, index


# ---------------------------------------------------------------------
# Encoding: bytes → B32K symbols
# ---------------------------------------------------------------------

def encode(data: bytes, symbols: List[str]) -> str:
    if not data:
        return ""

    # Length prefix for lossless decode (preserves leading 0x00 bytes)
    length_prefix = len(data).to_bytes(4, "big")
    payload = length_prefix + data

    bit_len = len(payload) * 8
    acc = int.from_bytes(payload, "big")

    groups = (bit_len + BITS_PER_SYMBOL - 1) // BITS_PER_SYMBOL
    pad_bits = groups * BITS_PER_SYMBOL - bit_len
    acc <<= pad_bits  # right-pad with zeros

    out: List[str] = []
    for i in range(groups):
        shift = (groups - 1 - i) * BITS_PER_SYMBOL
        val = (acc >> shift) & SYMBOL_MASK
        out.append(symbols[val])

    return "".join(out)


# ---------------------------------------------------------------------
# Decoding: B32K symbols → bytes
# ---------------------------------------------------------------------

def decode(text: str, index: Dict[str, int]) -> bytes:
    """
    Decode Base32768 text (fixed-width symbols) back into bytes.
    """
    if not text:
        return b""

    if len(text) % SYMBOL_CHARS != 0:
        raise ValueError("B32K text length is not aligned to symbol width")

    acc = 0
    symbols_count = len(text) // SYMBOL_CHARS

    for i in range(0, len(text), SYMBOL_CHARS):
        sym = text[i:i + SYMBOL_CHARS]
        try:
            v = index[sym]
        except KeyError:
            raise ValueError(f"Invalid B32K symbol: {sym!r}") from None
        acc = (acc << BITS_PER_SYMBOL) | v

    bit_len = symbols_count * BITS_PER_SYMBOL
    byte_len = bit_len // 8
    rem = bit_len - byte_len * 8
    if rem:
        acc >>= rem  # drop padding bits

    raw = acc.to_bytes(byte_len, "big")

    if len(raw) < 4:
        raise ValueError("B32K payload too short for length prefix")

    data_len = int.from_bytes(raw[:4], "big")
    if data_len < 0:
        raise ValueError("Invalid length prefix")

    out = raw[4:4 + data_len]
    if len(out) != data_len:
        raise ValueError("Truncated payload (length prefix exceeds decoded bytes)")

    return out
