"""Loopback-only B32K public kiosk daemon.

This module intentionally exposes one public projection: successful silence.
It does not expose arbitrary B32K mount forwarding.
"""

from __future__ import annotations

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import subprocess
from typing import Iterable
from urllib.parse import urlparse

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9325
KIOSK_ROUTE = ".b32k.3.2.1.xitadel.2.1"


@dataclass(frozen=True)
class KioskProjection:
    status: str = "intentional_silence"
    route: str = KIOSK_ROUTE
    role: str = "xitadel_kiosk"
    successful_noop: bool = True
    network_action_available: bool = False
    private_xitadel_not_exposed: bool = True
    network_exposure: str = "loopback_only"
    runtime_state_mutated: bool = False
    tower_mutated: bool = False
    authority_conferred: bool = False
    agency_conferred: bool = False
    truth_conferred: bool = False


def normalize_public_route(path: str) -> str:
    """Collapse every public route to the kiosk route."""
    return KIOSK_ROUTE


def poll_kiosk(argv: Iterable[str] | None = None) -> dict[str, object]:
    """Poll the private kiosk through the sealed B32K mount."""
    command = list(argv or [
        "b32k",
        "mount",
        "organization",
        "xitadel",
        "kiosk",
        "poll",
    ])
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "status": "kiosk_unavailable",
            "route": KIOSK_ROUTE,
            "role": "xitadel_kiosk",
            "successful_noop": False,
            "network_action_available": False,
            "private_xitadel_not_exposed": True,
            "network_exposure": "loopback_only",
            "runtime_state_mutated": False,
            "tower_mutated": False,
            "authority_conferred": False,
            "agency_conferred": False,
            "truth_conferred": False,
            "error": completed.stdout.strip(),
        }

    parsed: dict[str, object] = {}
    for line in completed.stdout.splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        if value == "true":
            parsed[key] = True
        elif value == "false":
            parsed[key] = False
        else:
            parsed[key] = value

    projection = KioskProjection().__dict__.copy()
    projection.update(parsed)
    projection["route"] = KIOSK_ROUTE
    projection["network_exposure"] = "loopback_only"
    projection["runtime_state_mutated"] = False
    projection["tower_mutated"] = False
    projection["authority_conferred"] = False
    projection["agency_conferred"] = False
    projection["truth_conferred"] = False
    return projection


class B32KDHandler(BaseHTTPRequestHandler):
    server_version = "b32kd/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = normalize_public_route(parsed.path)
        result = poll_kiosk()
        result["public_request_path"] = parsed.path
        result["normalized_route"] = route
        body = json.dumps(result, sort_keys=True, indent=2).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("cache-control", "no-store")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        self.send_error(405, "method not allowed")

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    if host != "127.0.0.1":
        raise RuntimeError("b32kd is currently restricted to 127.0.0.1")
    server = ThreadingHTTPServer((host, port), B32KDHandler)
    print(f"b32kd loopback kiosk running: http://{host}:{port}/")
    server.serve_forever()


def main() -> int:
    serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
