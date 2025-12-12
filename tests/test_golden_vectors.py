import json
from pathlib import Path

from spec.b32k.codec import load_b32k_alphabet, encode, decode

GOLDEN_PATH = Path(__file__).with_name("golden_vectors.json")
ALPHABET_PATH = Path("spec/b32k/b32k.json")


def test_golden_vectors_exist():
    assert GOLDEN_PATH.exists(), f"Missing {GOLDEN_PATH}. Run make_golden_vectors.py"


def test_golden_vectors_lock_codec_behavior():
    symbols, index = load_b32k_alphabet(ALPHABET_PATH)

    doc = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    vectors = doc["vectors"]

    for name, v in vectors.items():
        raw = bytes.fromhex(v["hex"])
        expected = v["b32k"]

        enc = encode(raw, symbols)
        dec = decode(enc, index)

        assert dec == raw, f"{name}: decode(encode(x)) mismatch"
        assert enc == expected, f"{name}: encoded output drifted (codec contract changed)"
