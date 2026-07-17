import os
from contextlib import contextmanager

MOUNT_PROTOCOL = "b32k.mount.v1"
ROOKOS_MOUNT_HANDLE = "b32k.3.2.1"
ROOKOS_MOUNT_TARGET = "rookos"

_ENVIRONMENT = {
    "B32K_MOUNT_PROTOCOL": MOUNT_PROTOCOL,
    "B32K_MOUNT_HANDLE": ROOKOS_MOUNT_HANDLE,
    "B32K_MOUNT_TARGET": ROOKOS_MOUNT_TARGET,
}


@contextmanager
def rookos_mount_environment():
    previous = {
        key: os.environ.get(key)
        for key in _ENVIRONMENT
    }
    os.environ.update(_ENVIRONMENT)
    try:
        yield dict(_ENVIRONMENT)
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
