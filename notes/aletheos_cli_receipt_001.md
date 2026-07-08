# Aletheos CLI RECEIPT 001

Timestamp: 2026-07-08T15:22:14

Status: pre-ratification CLI expansion.

This note records the first returned-trace receipt gate.

RECEIPT is deliberately narrow.

It does not accept a raw sentence.

It accepts a valid RETURN receipt JSON file.

This means the trace must first be marked, hashed, admitted, returned, and receipted before it becomes a returned trace body.

Example:

    python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
    python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json
    python scripts/aletheos_cli.py RETURN ~/tmp/admit.json --json > ~/tmp/return.json
    python scripts/aletheos_cli.py RECEIPT ~/tmp/return.json

Expected transition:

    RETURNED -> RECEIPTED

## Boundary

RECEIPT does not mean the trace is verified.

RECEIPT does not mean reliance is allowed.

RECEIPT does not assign a B32K index.

RECEIPT does not ratify the trace.

RECEIPT records that the returned trace now has a ledger body.

## Keeper

RECEIPT gives the returned trace a body without pretending verification is complete.
