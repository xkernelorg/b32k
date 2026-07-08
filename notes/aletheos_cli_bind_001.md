# Aletheos CLI BIND 001

Timestamp: 2026-07-08T15:34:29

Status: pre-ratification CLI expansion.

This note records the first binding gate.

BIND is deliberately narrow.

It does not accept a raw sentence.

It accepts a valid VERIFY receipt JSON file.

This means the trace must first be marked, admitted, returned, receipted, and verified before it can be bound.

Example:

    python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
    python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json
    python scripts/aletheos_cli.py RETURN ~/tmp/admit.json --json > ~/tmp/return.json
    python scripts/aletheos_cli.py RECEIPT ~/tmp/return.json --json > ~/tmp/receipt.json
    python scripts/aletheos_cli.py VERIFY ~/tmp/receipt.json --json > ~/tmp/verify.json
    python scripts/aletheos_cli.py BIND ~/tmp/verify.json

Expected transition:

    VERIFIED -> BOUND

## Boundary

BIND does not create commercial reliance.

BIND does not create sovereign reliance.

BIND does not assign a final B32K index.

BIND does not ratify the trace.

BIND attaches the verified trace to a pre-ratification lane, schema, and address.

## Keeper

BIND attaches the verified trace to a lane without pretending reliance has been granted.
