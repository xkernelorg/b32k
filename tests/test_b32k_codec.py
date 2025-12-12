import hashlib
from math import ceil

from spec.b32k.codec import load_b32k_alphabet, encode, decode


def _symbols_for_bytes(n_bytes: int) -> int:
    """
    Helper: number of Base32768 symbols required for n_bytes payload
    (including 4-byte length prefix).
    """
    payload_bytes = 4 + n_bytes
    return ceil((payload_bytes * 8) / 15)


def test_alphabet_loads_and_is_complete():
    symbols, index = load_b32k_alphabet("spec/b32k/b32k.json")

    # Alphabet size
    assert len(symbols) == 32768
    assert len(index) == 32768

    # Canonical contract: alphabet indices are 1-based
    assert symbols[0] == "~00001"
    assert symbols[1] == "~00002"
    assert symbols[-1] == "~32768"

    # Internal codec index remains 0-based
    assert index["~00001"] == 0
    assert index["~32768"] == 32767


def test_roundtrip_sha256_digest():
    symbols, index = load_b32k_alphabet("spec/b32k/b32k.json")

    data = hashlib.sha256(b"hello world").digest()
    enc = encode(data, symbols)
    dec = decode(enc, index)

    assert dec == data
    assert len(enc) == _symbols_for_bytes(len(data)) * 6  # 6 chars per symbol


def test_roundtrip_various_lengths_and_leading_zeros():
    symbols, index = load_b32k_alphabet("spec/b32k/b32k.json")

    samples = [
        b"",
        b"\x00",
        b"\x00\x00",
        b"\x00\x01",
        b"\x00\x01\x00",
        b"\x00\x00\x01",
        bytes(range(1)),
        bytes(range(2)),
        bytes(range(3)),
        bytes(range(7)),
        bytes(range(8)),
        bytes(range(15)),
        bytes(range(16)),
        bytes(range(31)),
        bytes(range(32)),
        bytes(range(33)),
        bytes(range(64)),
        bytes(range(127)),
    ]

    for data in samples:
        enc = encode(data, symbols)
        dec = decode(enc, index)
        assert dec == data


def test_decode_rejects_unaligned_length():
    _, index = load_b32k_alphabet("spec/b32k/b32k.json")

    try:
        decode("~0000", index)  # not divisible by SYMBOL_CHARS = 6
        assert False, "Expected ValueError for unaligned symbol length"
    except ValueError as e:
        assert "aligned" in str(e)


def test_decode_rejects_invalid_symbol():
    _, index = load_b32k_alphabet("spec/b32k/b32k.json")

    bad = "~99999"  # outside canonical alphabet
    try:
        decode(bad, index)
        assert False, "Expected ValueError for invalid symbol"
    except ValueError as e:
        assert "Invalid B32K symbol" in str(e)
