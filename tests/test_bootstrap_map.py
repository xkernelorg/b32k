import json
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B32KBootstrapMapTests(unittest.TestCase):
    def load(self):
        return json.loads(
            (
                ROOT
                / "artifacts/json/b32k_bootstrap_map_001.json"
            ).read_text()
        )

    def test_canonical_handle_map(self):
        handles = self.load()["handles"]

        self.assertEqual(handles["b32k.1"]["role"], "null_indexer")
        self.assertEqual(
            handles["b32k.2"]["role"],
            "self_referencing_bootloader",
        )
        self.assertEqual(
            handles["b32k.2.1"]["role"],
            "public_b32k_shell",
        )
        self.assertEqual(
            handles["b32k.3"]["role"],
            "organization_root",
        )
        self.assertEqual(
            handles["b32k.3.1.1"]["role"],
            "organization_bootloader",
        )
        self.assertEqual(
            handles["b32k.3.1.2"]["role"],
            "organization_api",
        )
        self.assertEqual(
            handles["b32k.4"]["role"],
            "first_ordinary_lane",
        )

    def test_top_level_positions_preserve_indexing_profile(self):
        handles = self.load()["handles"]

        self.assertEqual(handles["b32k.1"]["catalogue_address"], 1)
        self.assertEqual(handles["b32k.1"]["registered_index"], 0)
        self.assertEqual(handles["b32k.2"]["catalogue_address"], 2)
        self.assertEqual(handles["b32k.2"]["registered_index"], 1)
        self.assertEqual(handles["b32k.3"]["catalogue_address"], 3)
        self.assertEqual(handles["b32k.3"]["registered_index"], 2)
        self.assertEqual(handles["b32k.4"]["catalogue_address"], 4)
        self.assertEqual(handles["b32k.4"]["registered_index"], 3)

    def test_descendant_handles_do_not_consume_catalogue_positions(self):
        handles = self.load()["handles"]

        for handle in (
            "b32k.2.1",
            "b32k.3.1.1",
            "b32k.3.1.2",
        ):
            self.assertTrue(handles[handle]["descendant_context"])
            self.assertFalse(
                handles[handle]["registered_position_consumed"]
            )

    def test_bootloader_has_one_external_action(self):
        law = self.load()["bootstrap_law"]

        self.assertEqual(law["public_entry_handle"], "b32k.2.1")
        self.assertTrue(law["packet_identity_preserved"])
        self.assertEqual(
            law["sole_external_action"],
            {
                "action": "pipe_packet_unchanged",
                "authority_scope": "transport_only",
                "target": "b32k.3.1.1",
            },
        )

    def test_organization_api_remains_separately_gated(self):
        artifact = self.load()
        boundary = artifact["organization_boundary"]
        nonclaims = artifact["nonclaims"]

        self.assertEqual(
            boundary["organization_bootloader_handle"],
            "b32k.3.1.1",
        )
        self.assertEqual(
            boundary["api_handle"],
            "b32k.3.1.2",
        )
        self.assertTrue(
            boundary[
                "api_requires_separate_authentication_and_admission"
            ]
        )
        self.assertFalse(
            nonclaims["bootloader_invokes_organization_api"]
        )
        self.assertFalse(
            nonclaims["public_shell_access_confers_authority"]
        )
        self.assertFalse(
            nonclaims["public_shell_access_confers_trust"]
        )

    def test_profile_dependency_remains_pinned(self):
        dependency = self.load()["address_space_dependency"]

        self.assertEqual(
            dependency["profile_id"],
            "b32k.indexing.current-repo.002",
        )
        self.assertEqual(
            dependency["profile_sha256"],
            "341ddac255e7390118e0485be739c717fee76351361323329eb0e86f5cc525c3",
        )

    def test_package_version(self):
        project = tomllib.loads(
            (ROOT / "pyproject.toml").read_text()
        )
        self.assertEqual(project["project"]["version"], "0.6.0")


if __name__ == "__main__":
    unittest.main()
