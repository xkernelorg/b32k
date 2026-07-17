import unittest
from pathlib import Path
from unittest.mock import patch

from b32k.update import (
    B32KUpdateInspectionError,
    ComponentUpdate,
    inspect_component_update,
    registered_sources,
)


class UpdateInspectorTests(unittest.TestCase):
    def test_kernel_registration_is_canonical(self):
        source = registered_sources(Path("/home/test"))["kernel"]
        self.assertEqual(source.component, "kernel")
        self.assertEqual(source.branch, "main")
        self.assertEqual(
            source.repository_url,
            "git@github.com:xkernelorg/xkernel.git",
        )
        self.assertEqual(
            source.local_path,
            Path(
                "/home/test/dev/cori/research/computing/"
                "kernel/xkernel"
            ),
        )

    def test_unknown_component_fails_closed(self):
        with self.assertRaises(B32KUpdateInspectionError):
            inspect_component_update("unknown", fetch=False)

    def test_result_separates_check_from_activation(self):
        result = ComponentUpdate(
            component="kernel",
            repository_url="git@github.com:xkernelorg/xkernel.git",
            local_path="/tmp/xkernel",
            branch="main",
            local_commit="a" * 40,
            upstream_commit="b" * 40,
            ahead_count=0,
            behind_count=1,
            working_tree_clean=True,
            update_available=True,
            checked_at="2026-07-17T00:00:00+00:00",
            fetch_performed=True,
        )
        value = result.as_dict()
        self.assertTrue(value["update_available"])
        self.assertTrue(value["fetch_performed"])
        self.assertFalse(value["checkout_performed"])
        self.assertFalse(value["merge_performed"])
        self.assertFalse(value["installation_performed"])
        self.assertFalse(value["authority_conferred"])

    def test_inspection_uses_fixed_git_operations(self):
        root = Path("/home/test/dev/cori/research/computing/kernel/xkernel")
        outputs = iter([
            "git@github.com:xkernelorg/xkernel.git",
            "main",
            "",
            "a" * 40,
            "b" * 40,
            "0 1",
            "",
        ])

        with patch.object(Path, "is_dir", return_value=True), \
             patch.object(Path, "exists", return_value=True), \
             patch("b32k.update._git", side_effect=lambda *a, **k: next(outputs)):
            result = inspect_component_update(
                "kernel",
                fetch=True,
                home=Path("/home/test"),
            )

        self.assertEqual(result.local_path, str(root))
        self.assertEqual(result.behind_count, 1)
        self.assertTrue(result.update_available)
        self.assertTrue(result.fetch_performed)
        self.assertFalse(result.checkout_performed)


if __name__ == "__main__":
    unittest.main()
