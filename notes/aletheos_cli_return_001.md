# Aletheos CLI RETURN 001

Timestamp: 2026-07-08T15:21:02

Status: pre-ratification CLI expansion.

This note records the first return gate.

RETURN is deliberately narrow.

It does not accept a raw sentence.

It accepts a valid ADMIT receipt JSON file.

This means the trace must first be marked, hashed, receipted, and admitted before it can return from witness passage.

Example:

    python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
    python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json
    python scripts/aletheos_cli.py RETURN ~/tmp/admit.json

Expected transition:

    ADMITTED -> RETURNED

## Boundary

RETURN does not mean the trace is verified.

RETURN does not mean reliance is allowed.

RETURN does not assign a B32K index.

RETURN does not ratify the trace.

RETURN only records that an admitted trace came home from witness passage.

## Keeper

RETURN brings the trace home without pretending trust has been granted.
