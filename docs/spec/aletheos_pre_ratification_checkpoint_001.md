# Aletheos Pre-Ratification Checkpoint 001

Status: checkpoint.

## Purpose

This checkpoint records the current state of the B32K-Aletheos canonical profile after the first positive and negative witness packets.

It is a status checkpoint, not ratification.

## Current state

B32K is live as an external symbolic scaffold.

Aletheos is a pre-ratification binding profile over that scaffold.

No sovereign or commercial reliance is allowed yet.

Assignments may still change by receipt before ratification.

After ratification, addresses and receipts must not silently drift.

## Root constitution

Root lane:

    b32k.aletheos.bound.v1

Reserved root addresses:

    0 = NULL_WELL
    1 = ALETHEOS_ROOT

Zero is the well.

One is the witness root.

## Minimal apparatus

Under ALETHEOS_ROOT:

    boundary
    state
    logic
    language
    sequence
    memory
    I/O
    receipt
    body

Thesis:

    Boundary before body.
    Witness before authority.
    Receipt before trust.

## Operator discipline

A is local motion.

M is admission.

M^T is return.

Q is receipt.

Primary law:

    Q = M M^T

Reference identity:

    Q = M M^T = A^3 + 2A^2 + 2I

## Instruction grammar

Current opcodes:

    NOOP
    MARK
    ADMIT
    RETURN
    RECEIPT
    REJECT
    BIND
    VERIFY

Trust rule:

    Presence is not trust.
    No Q, no trust.

## Execution states

Current states:

    NULL
    MARKED
    ADMITTED
    RETURNED
    RECEIPTED
    BOUND
    VERIFIED
    REJECTED
    REVOKED

Only VERIFIED may carry positive reliance under subscriber policy.

## Witness packets

Positive witness packet:

    artifact: artifacts/json/aletheos_minimal_witness_packet_001.json
    claim: Boundary before body.
    route: NULL -> MARKED -> ADMITTED -> RETURNED -> RECEIPTED -> BOUND -> VERIFIED
    final_state: VERIFIED

Negative witness packet:

    artifact: artifacts/json/aletheos_negative_witness_packet_001.json
    claim attempted: Index 0 carries positive authority.
    route: NULL -> MARKED -> REJECTED
    final_state: REJECTED
    rejection_reason: index_0_positive_authority_denied

## Validation status

The validator currently checks:

    JSON parses
    canonical root index 0 and 1
    index 0 cannot carry positive authority
    operator profile law Q = M M^T
    required instruction opcodes
    required execution states
    minimal apparatus order
    positive witness packet shape
    negative witness packet shape
    bound KJV entries against the structural-key registry

## Not ratified

This checkpoint does not ratify the Aletheos binding profile.

Open before ratification:

    decide structural-key assignment policy
    harden canonical index schema
    harden witness packet schema enforcement
    decide lane naming stability
    review contract draft
    prepare ratification receipt
    tag release only after ratification

## Keeper

A machine that cannot refuse cannot be trusted.

Aletheos has now refused correctly.

The scaffold is live.

The binding is cooling.

The profile names the machine.

The first receipts prove it can say yes and no.
