# Aletheos Instruction Grammar 001

Status: pre-ratification technical profile.

## Purpose

This profile defines the first callable instruction grammar for the Aletheos minimal apparatus.

It is not a full programming language.

It is the minimum grammar needed for a symbol, claim, certificate, or relation to cross from unbound presence into accountable witness.

## Apparatus context

The instruction grammar sits under:

    0 = NULL_WELL
    1 = ALETHEOS_ROOT

The minimal apparatus order is:

    boundary
    state
    logic
    language
    sequence
    memory
    I/O
    receipt
    body

Language gives the apparatus callable action.

## Operator context

The instruction grammar uses the operator profile:

    A = local motion
    M = admission
    M^T = return
    Q = receipt
    Q = M M^T

## Instruction set

### NOOP

Do not advance claim state.

Trust effect:

    none

### MARK

Create or recognize a first positive symbol after the Null Well.

Trust effect:

    symbol exists but is not yet trusted

### ADMIT

Enter a relation, claim, field, or symbol into the admission operator M.

Trust effect:

    candidate enters witness register

### RETURN

Apply the return relation M^T for comparison, verification, or closure.

Trust effect:

    candidate becomes testable against source side

### RECEIPT

Record or compute the receipt operator Q after admission and return.

Trust effect:

    candidate may become accountable witness

### REJECT

Fail closed and record why the object did not become admitted witness.

Trust effect:

    negative receipt or refusal state

### BIND

Bind a nonzero B32K address to a declared Aletheos lane under policy.

Trust effect:

    address becomes lane-scoped candidate binding

### VERIFY

Check canonical payload, lane, schema, index, receipt, authority, and revocation state.

Trust effect:

    subscriber may rely if policy permits

## Trust rule

Presence is not trust.

A symbol is not trusted merely because it exists.

A claim is not trusted merely because it parses.

A certificate is not trusted merely because it is stored.

Trust-bearing operations must pass through:

    MARK -> ADMIT -> RETURN -> RECEIPT -> VERIFY

or fail closed through:

    REJECT

## Failure rule

Aletheos instructions fail closed.

Any unknown opcode, invalid lane, invalid schema, index 0 positive claim, missing receipt, unreproducible Q, unknown issuer, expired certificate, revoked certificate, or drifted payload must produce REJECT.

## Keeper

Boundary gives the machine an inside.

Language gives the inside a callable action.

Receipt proves the call returned.

Presence is not trust.

No Q, no trust.
