# Aletheos negative witness packet 001

Date: 2026-07-08

Artifact:

    artifacts/json/aletheos_negative_witness_packet_001.json

Claim attempted:

    Index 0 carries positive authority.

Expected result:

    REJECTED

Rejection reason:

    index_0_positive_authority_denied

Route:

    NULL -> MARKED -> REJECTED

Purpose:

    Prove that the current Aletheos canonical profile can fail closed when index 0 is treated as positive authority.

Boundary:

    This is a pre-ratification negative test vector.
    This is not sovereign reliance.
    This is not commercial reliance.
    This is not a full runtime VM.

Keeper:

    A machine that can only say yes is not a trust machine.
    Index 0 cannot be positive authority.
