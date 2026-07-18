import unittest
from unittest.mock import patch, Mock

from b32k.daemon import KIOSK_ROUTE, normalize_public_route, poll_kiosk, serve


class B32KDTests(unittest.TestCase):
    def test_every_public_route_collapses_to_kiosk(self):
        self.assertEqual(normalize_public_route("/"), KIOSK_ROUTE)
        self.assertEqual(normalize_public_route("/anything"), KIOSK_ROUTE)
        self.assertEqual(
            normalize_public_route("/b32k/3/2/1/xitadel/4/1/5"),
            KIOSK_ROUTE,
        )

    def test_poll_uses_only_kiosk_mount_command(self):
        completed = Mock()
        completed.returncode = 0
        completed.stdout = """status: intentional_silence
route: .b32k.3.2.1.xitadel.2.1
role: xitadel_kiosk
successful_noop: true
network_action_available: false
private_xitadel_not_exposed: true
network_exposure: none
runtime_state_mutated: false
tower_mutated: false
authority_conferred: false
agency_conferred: false
truth_conferred: false
"""
        with patch("b32k.daemon.subprocess.run", return_value=completed) as run:
            result = poll_kiosk()

        run.assert_called_once()
        self.assertEqual(
            run.call_args.args[0],
            [
                "b32k",
                "mount",
                "organization",
                "xitadel",
                "kiosk",
                "poll",
            ],
        )
        self.assertEqual(result["status"], "intentional_silence")
        self.assertEqual(result["route"], KIOSK_ROUTE)
        self.assertEqual(result["network_exposure"], "loopback_only")
        self.assertFalse(result["runtime_state_mutated"])
        self.assertFalse(result["tower_mutated"])
        self.assertFalse(result["authority_conferred"])

    def test_non_loopback_serve_is_rejected(self):
        with self.assertRaises(RuntimeError):
            serve("0.0.0.0", 9325)


if __name__ == "__main__":
    unittest.main()
