import hashlib

from spec.b32k.codec import load_b32k_alphabet, encode, decode


def test_roundtrip_hash():
    symbols, index = load_b32k_alphabet("spec/b32k/b32k.json")

    data = hashlib.sha256(b"test").digest()
    enc = encode(data, symbols)
    dec = decode(enc, index)

    assert dec == data
