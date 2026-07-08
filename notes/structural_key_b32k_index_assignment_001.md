# Structural key B32K index assignment 001

Date: 2026-07-08

This note accompanies:

    artifacts/json/structural_key_b32k_index_assignment_001.json

Purpose:

    Assign provisional B32K 15-bit symbol indices to the structural key registry.

Method:

    sha256(lane:key) mod 32768
    collision resolution by linear probing

Boundary:

    These are provisional symbolic addresses.
    They are not final semantic law.
    They are not doctrine claims.
    They are not hidden-code claims.
    They are not physics claims.

Use:

    This lets the Concordance Ledger begin addressing structural keys inside the B32K symbol space while preserving a clear boundary between address assignment and meaning.
