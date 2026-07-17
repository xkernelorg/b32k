import os
import unittest

from b32k.mount import rookos_mount_environment


class MountContextTests(unittest.TestCase):
    def test_context_is_scoped_and_nonpersistent(self):
        keys = (
            "B32K_MOUNT_PROTOCOL",
            "B32K_MOUNT_HANDLE",
            "B32K_MOUNT_TARGET",
        )
        before = {key: os.environ.get(key) for key in keys}

        with rookos_mount_environment() as context:
            self.assertEqual(
                context["B32K_MOUNT_PROTOCOL"],
                "b32k.mount.v1",
            )
            self.assertEqual(
                context["B32K_MOUNT_HANDLE"],
                "b32k.3.2.1",
            )
            self.assertEqual(
                context["B32K_MOUNT_TARGET"],
                "rookos",
            )

        after = {key: os.environ.get(key) for key in keys}
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
