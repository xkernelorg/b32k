# Aletheos Canonical Profile 001

Status: pre-ratification canonical profile.

## Purpose

This document names the current Aletheos machine.

It collects the root constitution, minimal apparatus, operator profile, instruction grammar, execution state model, ratification checklist, and sovereign trust registry contract into one profile.

This profile does not ratify the system.

It defines the current pre-ratification shape.

## Scaffold and binding

B32K is the symbolic scaffold.

Aletheos is the declared binding profile over that scaffold.

Aletheos does not claim all possible B32K usage.

Aletheos-bound objects are valid only within declared Aletheos lanes, schemas, receipts, authority boundaries, and subscriber policies.

## Root constitution

Root lane:

    b32k.aletheos.bound.v1

Reserved addresses:

    0 = NULL_WELL
    1 = ALETHEOS_ROOT

Zero is the well.

One is the witness root.

## Minimal apparatus

Under ALETHEOS_ROOT, the minimal apparatus order is:

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

## Operator profile

A is local motion.

M is admission.

M^T is return.

Q is receipt.

Primary law:

    Q = M M^T

Reference identity:

    Q = M M^T = A^3 + 2A^2 + 2I

## Instruction grammar

Current instruction set:

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

## Execution state model

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

## Ratification status

Current status:

    pre-ratification

B32K public scaffold is live.

Aletheos binding profile is cooling.

Assignments may still be changed by receipt before ratification.

No sovereign or commercial reliance is allowed yet.

After ratification, addresses and receipts must not silently drift.

## Component artifacts

- b32k_aletheos_canonical_index_001
- aletheos_minimal_apparatus_001
- aletheos_operator_profile_001
- aletheos_instruction_grammar_001
- aletheos_execution_state_model_001
- aletheos_ratification_checklist_001
- b32k_aletheos_sovereign_trust_registry_agreement_003

## Keeper

The scaffold is live.

The binding is cooling.

The parts exist.

This profile names the machine.

Ratification is the moment the address becomes promise.
