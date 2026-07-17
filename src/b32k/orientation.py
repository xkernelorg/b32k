"""Permanent B32K orientation handles and aliases."""

from __future__ import annotations

ALIASES = {
    "null": "b32k.1",
    "boot": "b32k.2",
    "shell": "b32k.2.1",
    "org": "b32k.3",
    "org.label": "b32k.3.1",
    "org.boot": "b32k.3.1.1",
    "org.crypto": "b32k.3.1.2",
    "org.api": "b32k.3.2.1",
    "lane": "b32k.4",
}

HANDLE_ROLES = {
    "b32k.1": "null indexer",
    "b32k.2": "self-referencing B32K bootloader",
    "b32k.2.1": "public B32K orientation shell",
    "b32k.3": "organization root",
    "b32k.3.1": "permanent public organization label",
    "b32k.3.1.1": "organization bootloader",
    "b32k.3.1.2": "public cryptographic disclosure",
    "b32k.3.2.1": "organization API",
    "b32k.4": "first ordinary lane",
}


class B32KOrientationError(ValueError):
    """Raised when a handle or permanent alias cannot be resolved."""


def resolve_handle(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise B32KOrientationError("B32K handle or alias is required")

    token = value.strip().lower()
    canonical = ALIASES.get(token, token)

    if canonical not in HANDLE_ROLES:
        raise B32KOrientationError(
            f"unknown B32K handle or alias: {value}"
        )
    return canonical


def orientation_rows():
    for alias, handle in ALIASES.items():
        yield {
            "alias": alias,
            "handle": handle,
            "role": HANDLE_ROLES[handle],
        }
