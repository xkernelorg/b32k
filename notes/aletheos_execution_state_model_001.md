# Aletheos execution state model 001

Date: 2026-07-08

Files:

    docs/spec/aletheos_execution_state_model_001.md
    artifacts/json/aletheos_execution_state_model_001.json

Decision:

    Add the first state model for the Aletheos minimal apparatus.

States:

    NULL
    MARKED
    ADMITTED
    RETURNED
    RECEIPTED
    BOUND
    VERIFIED
    REJECTED
    REVOKED

Normal route:

    NULL -> MARKED -> ADMITTED -> RETURNED -> RECEIPTED -> BOUND -> VERIFIED

Trust rule:

    Presence is not trust.
    No Q, no trust.
    Only VERIFIED may carry positive reliance under subscriber policy.

Boundary:

    This is not a full runtime VM.
    This is not a B32K index assignment.
    This is a pre-ratification Aletheos state model.
