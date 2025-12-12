"""
Canonical Base32768 (B32K) codec

One symbol = 15 bits
Canonical transport symbol (ASCII) is the INDEX token: "~00000" .. "~32767"

This module implements the canonical bijection defining the
B32K Canonical Action Lattice (CAL-32K).
Behavior is locked by golden vectors.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict
from importlib import resources
# CAL-32K — B32K Canonical Action Lattice

BITS_PER_SYMBOL = 15
SYMBOL_CHARS = 6  # "~" + 5 digits
SYMBOL_MASK = (1 << BITS_PER_SYMBOL) - 1  # 0x7FFF


# ---------------------------------------------------------------------
# Alphabet loading (canonical)
# ---------------------------------------------------------------------
def load_b32k_alphabet(path: str | None = None) -> tuple[list[str], dict[str, int]]:
    """
    Load the canonical B32K alphabet JSON.

    Returns:
        (symbols, index)
        - symbols: list of 32768 fixed-width tokens (e.g. "~00001" .. "~32768")
        - index:   dict mapping token -> 0-based integer value
    """
    if path is not None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        with resources.files("b32k").joinpath("b32k.json").open("r", encoding="utf-8") as f:
            data = json.load(f)

    # Accept either {"symbols":[...]} or raw list [...]
    symbols = data["symbols"] if isinstance(data, dict) else data

    if len(symbols) != 32768:
        raise ValueError(f"Expected 32768 symbols, got {len(symbols)}")

    index = {sym: i for i, sym in enumerate(symbols)}
    return symbols, index
# ---------------------------------------------------------------------
# Encoding: bytes → B32K symbols
# ---------------------------------------------------------------------
def encode(data: bytes, symbols: List[str]) -> str:
    if not data:
        return ""

    # Length prefix for lossless decode (preserves leading 0x00 bytes)
    payload = len(data).to_bytes(4, "big") + data
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
        sym = text[i : i + SYMBOL_CHARS]
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
    out = raw[4 : 4 + data_len]
    if len(out) != data_len:
        raise ValueError("Truncated payload (length prefix exceeds decoded bytes)")

    return out
