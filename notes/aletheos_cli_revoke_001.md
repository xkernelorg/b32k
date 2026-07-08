# Aletheos CLI REVOKE 001

Timestamp: 2026-07-08T15:37:34

Status: pre-ratification CLI expansion.

This note records the first revocation gate.

REVOKE is deliberately narrow.

It does not accept a raw sentence.

It accepts a valid BIND receipt JSON file.

This means the trace must first be marked, admitted, returned, receipted, verified, and bound before it can be revoked.

Example:

    python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
    python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json --json > ~/tmp/admit.json
    python scripts/aletheos_cli.py RETURN ~/tmp/admit.json --json > ~/tmp/return.json
    python scripts/aletheos_cli.py RECEIPT ~/tmp/return.json --json > ~/tmp/receipt.json
    python scripts/aletheos_cli.py VERIFY ~/tmp/receipt.json --json > ~/tmp/verify.json
    python scripts/aletheos_cli.py BIND ~/tmp/verify.json --json > ~/tmp/bind.json
    python scripts/aletheos_cli.py REVOKE ~/tmp/bind.json

Expected transition:

    BOUND -> REVOKED

## Boundary

REVOKE does not erase history.

REVOKE does not delete prior receipts.

REVOKE does not ratify the trace.

REVOKE does not assign a B32K index.

REVOKE denies future reliance while preserving the receipt chain.

## Keeper

REVOKE denies future reliance without erasing the trace.
