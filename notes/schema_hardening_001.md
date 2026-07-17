# Schema hardening 001

Date: 2026-07-08

Purpose:

    Strengthen the filesystem ledger before adding Genesis 2.

Adds:

    artifacts/schema/kjv_chapter_structural_concordance.schema.json

Updates:

    scripts/validate_b32k_artifacts.py

Checks:

    JSON parsing
    artifact ids
    structural key uniqueness
    B32K wire/lane index range 0..32767; catalogue address range 1..32768
    Genesis/KJV entry id uniqueness
    known structural keys
    entry index matches registry index
    binding status present
    required entry fields present

Boundary:

    This hardens artifact shape only.
    It does not add doctrine claims, hidden-code claims, or physics claims.
