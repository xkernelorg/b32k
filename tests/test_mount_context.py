import json
import os
import unittest

from b32k.mount import (
    MOUNT_PROTOCOL,
    ROOKOS_MOUNT_HANDLE,
    ROOKOS_MOUNT_TARGET,
    build_rookos_mount_packet,
    rookos_mount_environment,
)


class MountContextTests(unittest.TestCase):
    def test_mount_context_sets_and_restores_environment(self):
        for key in (
            "B32K_MOUNT_PROTOCOL",
            "B32K_MOUNT_HANDLE",
            "B32K_MOUNT_TARGET",
            "B32K_MOUNT_PACKET",
            "B32K_MOUNT_PACKET_ID",
        ):
            self.assertIsNone(os.environ.get(key))

        argv = ["organization", "show"]
        with rookos_mount_environment(argv) as context:
            self.assertEqual(
                context["B32K_MOUNT_PROTOCOL"],
                MOUNT_PROTOCOL,
            )
            self.assertEqual(
                context["B32K_MOUNT_HANDLE"],
                ROOKOS_MOUNT_HANDLE,
            )
            self.assertEqual(
                context["B32K_MOUNT_TARGET"],
                ROOKOS_MOUNT_TARGET,
            )
            self.assertTrue(os.path.isfile(context["B32K_MOUNT_PACKET"]))

            with open(
                context["B32K_MOUNT_PACKET"],
                encoding="utf-8",
            ) as handle:
                packet = json.loads(handle.read())
            self.assertEqual(packet["argv"], argv)
            self.assertEqual(
                packet["packet_id"],
                context["B32K_MOUNT_PACKET_ID"],
            )
            self.assertFalse(packet["claims"]["authority_conferred"])

        for key in (
            "B32K_MOUNT_PROTOCOL",
            "B32K_MOUNT_HANDLE",
            "B32K_MOUNT_TARGET",
            "B32K_MOUNT_PACKET",
            "B32K_MOUNT_PACKET_ID",
        ):
            self.assertIsNone(os.environ.get(key))

    def test_mount_packet_identity_changes_with_argv(self):
        first = build_rookos_mount_packet(["organization", "show"])
        second = build_rookos_mount_packet([
            "organization",
            "xitadel",
            "kiosk",
            "poll",
        ])
        self.assertNotEqual(first["packet_id"], second["packet_id"])
        self.assertEqual(first["protocol"], "b32k.mount.v1")
        self.assertFalse(
            first["claims"]["principal_authenticated"]
        )


if __name__ == "__main__":
    unittest.main()
