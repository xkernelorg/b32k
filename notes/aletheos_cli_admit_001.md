# Aletheos CLI ADMIT 001

Timestamp: 2026-07-08T15:16:32

Status: pre-ratification CLI expansion.

This note records the first admission gate.

ADMIT is deliberately narrow.

It does not accept a raw sentence.

It accepts a valid MARK receipt JSON file.

This means the trace must first be marked, hashed, and receipted before it can enter the admission passage.

Example:

    python scripts/aletheos_cli.py MARK "open the door" --json > ~/tmp/mark.json
    python scripts/aletheos_cli.py ADMIT ~/tmp/mark.json

Expected transition:

    MARKED -> ADMITTED

## Boundary

ADMIT does not mean the trace is true.

ADMIT does not mean the trace has returned.

ADMIT does not mean Q has been formed.

ADMIT does not verify the trace.

ADMIT does not create reliance.

ADMIT only opens witness passage for a valid MARK receipt.

## Keeper

ADMIT opens the passage without pretending the return has happened.
