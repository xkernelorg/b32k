import json
import tomllib
import unittest
from pathlib import Path

from b32k.orientation import ALIASES, resolve_handle

ROOT = Path(__file__).resolve().parents[1]


class B32KBootstrapMap002Tests(unittest.TestCase):
    def load(self):
        return json.loads(
            (
                ROOT
                / "artifacts/json/b32k_bootstrap_map_002.json"
            ).read_text()
        )

    def test_map_002_supersedes_map_001(self):
        artifact = self.load()
        self.assertEqual(
            artifact["supersedes"],
            "b32k_bootstrap_map_001",
        )

    def test_public_and_execution_surfaces(self):
        handles = self.load()["handles"]
        expected = {
            "b32k.3.1": "permanent_public_organization_label",
            "b32k.3.1.1": "organization_bootloader",
            "b32k.3.1.2": "public_cryptographic_disclosure",
            "b32k.3.2": "organization_execution_surface",
            "b32k.3.2.1": "organization_api",
        }
        for handle, role in expected.items():
            self.assertEqual(handles[handle]["role"], role)
            self.assertFalse(
                handles[handle]["registered_position_consumed"]
            )

    def test_artifact_aliases_match_runtime_aliases(self):
        self.assertEqual(
            self.load()["alias_law"]["aliases"],
            ALIASES,
        )

    def test_permanent_alias_resolution(self):
        self.assertEqual(resolve_handle("shell"), "b32k.2.1")
        self.assertEqual(resolve_handle("org"), "b32k.3")
        self.assertEqual(
            resolve_handle("org.label"),
            "b32k.3.1",
        )
        self.assertEqual(
            resolve_handle("org.crypto"),
            "b32k.3.1.2",
        )
        self.assertEqual(
            resolve_handle("org.api"),
            "b32k.3.2.1",
        )

    def test_api_echoes_orientation_without_invocation(self):
        echo = self.load()["api_orientation_echo"]
        self.assertEqual(
            echo["orientation_shell"],
            "b32k.2.1",
        )
        self.assertEqual(
            echo["public_cryptographic_disclosure"],
            "b32k.3.1.2",
        )
        self.assertFalse(echo["echo_is_invocation"])
        self.assertFalse(echo["echo_is_redirect"])

    def test_mount_boundary(self):
        boundary = self.load()["implementation_boundary"]
        self.assertFalse(boundary["cli_mount_confers_authority"])
        self.assertFalse(boundary["cli_mount_installs_target"])
        self.assertFalse(
            boundary["cli_mount_mutates_target_state"]
        )

    def test_package_version(self):
        project = tomllib.loads(
            (ROOT / "pyproject.toml").read_text()
        )
        self.assertEqual(project["project"]["version"], "0.8.0")


if __name__ == "__main__":
    unittest.main()
