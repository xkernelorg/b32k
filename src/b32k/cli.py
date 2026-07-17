"""Human-facing B32K orientation and mount CLI."""

from __future__ import annotations
from b32k.mount import rookos_mount_environment

import argparse
import importlib
import shlex
from collections.abc import Sequence

from b32k.orientation import (
    B32KOrientationError,
    HANDLE_ROLES,
    orientation_rows,
    resolve_handle,
)

EXIT_SUCCESS = 0
EXIT_INVALID_REQUEST = 2
EXIT_TARGET_UNAVAILABLE = 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="b32k",
        description=(
            "B32K orientation shell and local target mount surface"
        ),
    )
    commands = parser.add_subparsers(dest="command")

    commands.add_parser(
        "orient",
        help="show permanent B32K orientation aliases",
    )

    resolve = commands.add_parser(
        "resolve",
        help="resolve a permanent alias or canonical handle",
    )
    resolve.add_argument("value")

    get = commands.add_parser(
        "get",
        help="get a B32K handle; the shell handle starts the shell",
    )
    get.add_argument("value")

    commands.add_parser(
        "shell",
        help="start the local B32K orientation shell",
    )

    mount = commands.add_parser(
        "mount",
        help="mount a local target through B32K orientation",
    )
    mount.add_argument("target")

    return parser


def print_orientation() -> None:
    print("B32K orientation")
    for row in orientation_rows():
        print(
            f"{row['alias']:<12} "
            f"{row['handle']:<14} "
            f"{row['role']}"
        )


def mount_rookos(argv: Sequence[str]) -> int:
    try:
        module = importlib.import_module("rookos.cli")
    except (ImportError, ModuleNotFoundError) as exc:
        print("status: target_unavailable")
        print("target: rookos")
        print(f"reason: {exc}")
        return EXIT_TARGET_UNAVAILABLE

    entry = getattr(module, "main", None)
    if not callable(entry):
        print("status: target_unavailable")
        print("target: rookos")
        print("reason: rookos.cli.main is unavailable")
        return EXIT_TARGET_UNAVAILABLE

    return int(entry(list(argv)))


def mount_target(target: str, argv: Sequence[str]) -> int:
    if target.lower() != "rookos":
        print("status: target_unavailable")
        print(f"target: {target}")
        print("reason: no B32K mount adapter is registered")
        return EXIT_TARGET_UNAVAILABLE

    forwarded = list(argv)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]
    with rookos_mount_environment():
        return mount_rookos(forwarded)


def interactive_shell() -> int:
    print_orientation()
    print("")
    print("Commands: where, resolve NAME, mount rookos, exit")

    while True:
        try:
            raw = input("b32k> ")
        except (EOFError, KeyboardInterrupt):
            print("")
            return EXIT_SUCCESS

        try:
            parts = shlex.split(raw)
        except ValueError as exc:
            print(f"status: invalid_request")
            print(f"reason: {exc}")
            continue

        if not parts:
            continue

        command = parts[0].lower()

        if command in ("exit", "quit"):
            return EXIT_SUCCESS

        if command in ("where", "orient"):
            print_orientation()
            continue

        if command == "resolve" and len(parts) == 2:
            try:
                handle = resolve_handle(parts[1])
            except B32KOrientationError as exc:
                print("status: invalid_request")
                print(f"reason: {exc}")
                continue
            print(f"{parts[1]} -> {handle}")
            print(f"role: {HANDLE_ROLES[handle]}")
            continue

        if (
            command == "mount"
            and len(parts) >= 2
        ):
            mount_target(parts[1], parts[2:])
            continue

        print("status: invalid_request")
        print("reason: unknown or malformed shell command")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args, remainder = parser.parse_known_args(argv)

    if args.command is None:
        print_orientation()
        return EXIT_SUCCESS

    if args.command != "mount" and remainder:
        parser.error(
            "unrecognized arguments: " + " ".join(remainder)
        )

    if args.command == "orient":
        print_orientation()
        return EXIT_SUCCESS

    if args.command == "resolve":
        try:
            handle = resolve_handle(args.value)
        except B32KOrientationError as exc:
            print("status: invalid_request")
            print(f"reason: {exc}")
            return EXIT_INVALID_REQUEST

        print(f"input: {args.value}")
        print(f"handle: {handle}")
        print(f"role: {HANDLE_ROLES[handle]}")
        return EXIT_SUCCESS

    if args.command == "get":
        try:
            handle = resolve_handle(args.value)
        except B32KOrientationError as exc:
            print("status: invalid_request")
            print(f"reason: {exc}")
            return EXIT_INVALID_REQUEST

        if handle == "b32k.2.1":
            return interactive_shell()

        print(f"handle: {handle}")
        print(f"role: {HANDLE_ROLES[handle]}")
        return EXIT_SUCCESS

    if args.command == "shell":
        return interactive_shell()

    if args.command == "mount":
        return mount_target(args.target, remainder)

    parser.error("unknown command")
    return EXIT_INVALID_REQUEST


if __name__ == "__main__":
    raise SystemExit(main())
