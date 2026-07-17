import io
import types
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from b32k.cli import (
    EXIT_SUCCESS,
    main,
    mount_rookos,
)


class B32KCLITests(unittest.TestCase):
    def capture(self, argv):
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(argv)
        return status, output.getvalue()

    def test_orient_lists_permanent_aliases(self):
        status, output = self.capture(["orient"])
        self.assertEqual(status, EXIT_SUCCESS)
        self.assertIn("shell", output)
        self.assertIn("b32k.2.1", output)
        self.assertIn("org.api", output)
        self.assertIn("b32k.3.2.1", output)

    def test_resolve_org_api(self):
        status, output = self.capture(
            ["resolve", "org.api"]
        )
        self.assertEqual(status, EXIT_SUCCESS)
        self.assertIn("handle: b32k.3.2.1", output)

    def test_get_non_shell_handle_is_noninteractive(self):
        status, output = self.capture(["get", "org.crypto"])
        self.assertEqual(status, EXIT_SUCCESS)
        self.assertIn("handle: b32k.3.1.2", output)

    def test_mount_forwards_arguments_to_rookos(self):
        observed = {}

        def fake_main(argv):
            observed["argv"] = argv
            return 7

        fake_module = types.SimpleNamespace(main=fake_main)

        with patch(
            "b32k.cli.importlib.import_module",
            return_value=fake_module,
        ):
            status = mount_rookos(
                ["organization", "show"]
            )

        self.assertEqual(status, 7)
        self.assertEqual(
            observed["argv"],
            ["organization", "show"],
        )


if __name__ == "__main__":
    unittest.main()
