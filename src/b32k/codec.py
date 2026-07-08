# src/b32k/codec.py
from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Dict, List, Tuple


def _symbols_from_alphabet_rows(rows: list) -> List[str]:
    """
    Compile the 32768-symbol alphabet from canonical b32k.json alphabet.rows.

    Each row is a dict containing:
      - unicode_point: e.g. "U+0001"
      - hex: e.g. "0x0001"

    We accept either field and interpret it as a hex codepoint.
    """
    symbols: List[str] = []

    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"Invalid alphabet row type: {type(row).__name__}")

        up = row.get("unicode_point") or row.get("hex")
        if not isinstance(up, str):
            raise ValueError("Alphabet row missing unicode_point/hex")

        s = up.strip().upper().replace("U+", "").replace("0X", "")
        codepoint = int(s, 16)
        symbols.append(chr(codepoint))

    if len(symbols) != 32768:
        raise ValueError(f"Expected 32768 symbols, got {len(symbols)}")

    return symbols


def load_b32k_alphabet(path: str | None = None) -> Tuple[List[str], Dict[str, int]]:
    """
    Load the canonical B32K alphabet.

    Supported formats:
      1. Raw list[str]
      2. {"symbols": list[str]}
      3. Canonical b32k.json with alphabet.rows
    """
    if path is not None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        with resources.files("b32k").joinpath("b32k.json").open("r", encoding="utf-8") as f:
            data = json.load(f)

    # Case 1: raw list
    if isinstance(data, list):
        symbols = data

    # Case 2: legacy wrapper
    elif isinstance(data, dict) and "symbols" in data:
        symbols = data["symbols"]

    # Case 3: canonical schema
    elif isinstance(data, dict) and "alphabet" in data:
        rows = data["alphabet"].get("rows")
        if not isinstance(rows, list):
            raise ValueError("alphabet.rows must be a list")
        symbols = _symbols_from_alphabet_rows(rows)

    else:
        raise ValueError(f"Unrecognized alphabet container type: {type(data).__name__}")

    if len(symbols) != 32768:
        raise ValueError(f"Expected 32768 symbols, got {len(symbols)}")

    index = {sym: i for i, sym in enumerate(symbols)}
    return symbols, index


# -----------------------------
# Framing helpers (NO guessing)
# -----------------------------

def _frame(data: bytes) -> bytes:
    """Prefix payload with 4-byte big-endian length."""
    return len(data).to_bytes(4, "big") + data


def _unframe(data: bytes) -> bytes:
    """Strip payload using 4-byte big-endian length."""
    if len(data) < 4:
        raise ValueError("Decoded data too short to contain length prefix")
    n = int.from_bytes(data[:4], "big")
    return data[4 : 4 + n]


# -----------------------------
# Base32768 codec (LSB-first)
# -----------------------------

def encode(data: bytes, symbols: List[str]) -> str:
    """
    Encode bytes into Base32768 string.

    IMPORTANT: This codec is bit-packed and may pad trailing bits. To make
    decode(encode(x)) == x always true, we LENGTH-FRAME the payload.
    """
    data = _frame(data)

    out: List[str] = []
    bitbuf = 0
    bitlen = 0

    for b in data:
        bitbuf |= b << bitlen
        bitlen += 8

        while bitlen >= 15:
            out.append(symbols[bitbuf & 0x7FFF])
            bitbuf >>= 15
            bitlen -= 15

    if bitlen:
        out.append(symbols[bitbuf & 0x7FFF])

    return "".join(out)


def decode(text: str, index: Dict[str, int]) -> bytes:
    """
    Decode Base32768 string back to bytes.

    Because encode() length-frames the input, we unframe here and ignore any
    trailing padding that arises from 15-bit symbol packing.
    """
    out = bytearray()
    bitbuf = 0
    bitlen = 0

    for ch in text:
        bitbuf |= index[ch] << bitlen
        bitlen += 15

        while bitlen >= 8:
            out.append(bitbuf & 0xFF)
            bitbuf >>= 8
            bitlen -= 8

    return _unframe(bytes(out))
