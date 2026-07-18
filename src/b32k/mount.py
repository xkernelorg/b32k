import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path


MOUNT_PROTOCOL = "b32k.mount.v1"
ROOKOS_MOUNT_HANDLE = "b32k.3.2.1"
ROOKOS_MOUNT_TARGET = "rookos"
MOUNT_PACKET_VERSION = "0.1.0"


def canonical_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def argv_hash(argv):
    return canonical_hash(list(argv))


def build_rookos_mount_packet(argv):
    body = {
        "schema_version": MOUNT_PACKET_VERSION,
        "packet_type": "b32k.mount.packet",
        "protocol": MOUNT_PROTOCOL,
        "handle": ROOKOS_MOUNT_HANDLE,
        "target": ROOKOS_MOUNT_TARGET,
        "argv_hash": argv_hash(argv),
        "argv": list(argv),
        "claims": {
            "authority_conferred": False,
            "principal_authenticated": False,
            "runtime_state_mutated": False,
            "target_state_mutated_by_mount": False,
            "network_exposure": "none",
        },
    }
    return {
        **body,
        "packet_id": "sha256:" + canonical_hash(body),
    }


def write_mount_packet(argv, directory=None):
    packet = build_rookos_mount_packet(argv)
    root = Path(directory) if directory is not None else Path(
        tempfile.gettempdir()
    )
    root.mkdir(parents=True, exist_ok=True)
    digest = packet["packet_id"].removeprefix("sha256:")
    path = root / f"b32k-mount-{digest}.json"
    path.write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path, packet


@contextmanager
def rookos_mount_environment(argv=()):
    path, packet = write_mount_packet(argv)
    previous = {
        "B32K_MOUNT_PROTOCOL": os.environ.get("B32K_MOUNT_PROTOCOL"),
        "B32K_MOUNT_HANDLE": os.environ.get("B32K_MOUNT_HANDLE"),
        "B32K_MOUNT_TARGET": os.environ.get("B32K_MOUNT_TARGET"),
        "B32K_MOUNT_PACKET": os.environ.get("B32K_MOUNT_PACKET"),
        "B32K_MOUNT_PACKET_ID": os.environ.get("B32K_MOUNT_PACKET_ID"),
    }
    context = {
        "B32K_MOUNT_PROTOCOL": MOUNT_PROTOCOL,
        "B32K_MOUNT_HANDLE": ROOKOS_MOUNT_HANDLE,
        "B32K_MOUNT_TARGET": ROOKOS_MOUNT_TARGET,
        "B32K_MOUNT_PACKET": str(path),
        "B32K_MOUNT_PACKET_ID": packet["packet_id"],
    }
    os.environ.update(context)
    try:
        yield context
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        path.unlink(missing_ok=True)
