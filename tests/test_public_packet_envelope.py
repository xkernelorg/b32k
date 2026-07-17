import copy
import json
import tomllib
import unittest
from pathlib import Path

from b32k.packet import (
    B32KPacketInadmissible,
    build_public_hello,
    inspect_public_packet,
    public_packet_id,
)

ROOT = Path(__file__).resolve().parents[1]


class PublicPacketEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.packet = build_public_hello(
            handle="b32k.2.1",
            client_nonce=(
                "client_nonce_0123456789abcdef"
            ),
            payload_visibility="opaque",
            payload_encoding="opaque",
            payload_content="",
        ).record

    def test_default_hello_round_trips(self):
        inspected = inspect_public_packet(self.packet)
        self.assertEqual(inspected.handle, "b32k.2.1")
        self.assertEqual(inspected.handshake_phase, "hello")
        self.assertEqual(
            inspected.packet_id,
            public_packet_id(self.packet),
        )

    def test_packet_id_excludes_only_itself(self):
        changed = copy.deepcopy(self.packet)
        changed["payload"]["content"] = "different"
        self.assertNotEqual(
            self.packet["packet_id"],
            public_packet_id(changed),
        )

    def test_tampering_is_rejected(self):
        changed = copy.deepcopy(self.packet)
        changed["handle"] = "b32k.3.2.1"
        with self.assertRaises(B32KPacketInadmissible):
            inspect_public_packet(changed)

    def test_reusable_password_is_rejected(self):
        changed = copy.deepcopy(self.packet)
        changed["handshake"]["password"] = "not-allowed"
        changed["packet_id"] = public_packet_id(changed)
        with self.assertRaises(B32KPacketInadmissible):
            inspect_public_packet(changed)

    def test_shape_does_not_claim_trust(self):
        artifact = json.loads(
            (
                ROOT
                / "artifacts/json/"
                "b32k_public_packet_envelope_001.json"
            ).read_text()
        )
        nonclaims = artifact["nonclaims"]
        self.assertFalse(
            nonclaims["valid_shape_confers_trust"]
        )
        self.assertFalse(
            nonclaims["valid_shape_confers_authentication"]
        )
        self.assertFalse(
            nonclaims["valid_shape_confers_authority"]
        )
        self.assertFalse(
            nonclaims["packet_id_is_encryption"]
        )

    def test_handshake_declares_three_phases(self):
        artifact = json.loads(
            (
                ROOT
                / "artifacts/json/"
                "b32k_public_packet_envelope_001.json"
            ).read_text()
        )
        self.assertEqual(
            set(artifact["handshake"]["phases"]),
            {"hello", "challenge", "proof"},
        )
        self.assertFalse(
            artifact["handshake"][
                "reusable_password_transmitted"
            ]
        )

    def test_package_version(self):
        project = tomllib.loads(
            (ROOT / "pyproject.toml").read_text()
        )
        self.assertEqual(
            project["project"]["version"],
            "0.8.0",
        )


if __name__ == "__main__":
    unittest.main()
