# Witness packet schema 001

Date: 2026-07-08

Purpose:

    Add first schema and validator checks for Aletheos witness packets.

Adds:

    artifacts/schema/aletheos_witness_packet.schema.json

Updates:

    scripts/validate_b32k_artifacts.py

Checks:

    route starts from NULL
    final_state is VERIFIED
    final_state matches route end
    normal positive route is preserved
    normal instruction route is preserved
    MARK, ADMIT, RETURN, RECEIPT, BIND, VERIFY are present
    no_q_no_trust is asserted
    verified_only is asserted
    payload hash exists
    route digest exists
    commercial and sovereign reliance are false pre-ratification

Keeper:

    The first witness ran.
    Now the ledger can recognize its voice.
