# Aletheos CLI VERIFY 001

Timestamp: 2026-07-08T15:23:41

Status: pre-ratification CLI expansion.

This note records the first verification gate.

VERIFY is deliberately narrow.

It does not accept a raw sentence.

It accepts a valid RECEIPT receipt JSON file.

This means the trace must first be marked, admitted, returned, and receipted before it can be verified.

Example:

    python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
    python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json
    python scripts/aletheos_cli.py RETURN ~/tmp/admit.json --json > ~/tmp/return.json
    python scripts/aletheos_cli.py RECEIPT ~/tmp/return.json --json > ~/tmp/receipt.json
    python scripts/aletheos_cli.py VERIFY ~/tmp/receipt.json

Expected transition:

    RECEIPTED -> VERIFIED

## Boundary

VERIFY checks internal chain shape and hashes.

VERIFY does not create commercial reliance.

VERIFY does not create sovereign reliance.

VERIFY does not assign a B32K index.

VERIFY does not ratify the trace.

VERIFY is still pre-ratification.

## Keeper

VERIFY checks the chain without pretending ratification has happened.
