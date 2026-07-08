# Schema alignment 001

Date: 2026-07-08

Purpose:

    Align the schema and validator layer with the Aletheos minimal apparatus, operator profile, instruction grammar, and execution state model.

Adds schemas:

    artifacts/schema/aletheos_operator_profile.schema.json
    artifacts/schema/aletheos_instruction_grammar.schema.json
    artifacts/schema/aletheos_execution_state_model.schema.json
    artifacts/schema/aletheos_minimal_apparatus.schema.json

Updates validator:

    scripts/validate_b32k_artifacts.py

Validation now checks:

    NULL_WELL at index 0
    ALETHEOS_ROOT at index 1
    Q = M M^T
    required instruction opcodes
    required execution states
    no_q_no_trust
    positive reliance state is VERIFIED
    minimal apparatus order
    bound KJV entries still match structural-key registry

Boundary:

    This is first-pass schema alignment, not final ratification.
