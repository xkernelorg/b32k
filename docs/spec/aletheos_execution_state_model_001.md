# Aletheos Execution State Model 001

Status: pre-ratification technical profile.

## Purpose

This profile defines the first execution state model for the Aletheos minimal apparatus.

The instruction grammar defines callable actions.

The execution state model defines where an object is in its journey from Null Well to verified witness, or to failure.

## State model

### NULL

Unbound. No admitted binding. No positive claim. No authority.

### MARKED

A first positive symbol or object exists after the Null Well, but is not yet trusted.

### ADMITTED

The object has entered the admission operator M under a declared boundary, lane, and schema.

### RETURNED

The object has passed through the return relation M^T for comparison, verification, or closure.

### RECEIPTED

The object has produced a reproducible receipt Q.

### BOUND

The object is bound to a nonzero B32K address inside a declared Aletheos lane.

### VERIFIED

The object has passed verification under the relevant subscriber, lane, receipt, authority, and revocation policy.

### REJECTED

The object failed closed and must not be treated as positive authority.

### REVOKED

A previously valid or relied-upon object has been revoked. Its receipt remains, but reliance is denied.

## Normal route

The normal positive route is:

    NULL -> MARKED -> ADMITTED -> RETURNED -> RECEIPTED -> BOUND -> VERIFIED

The operator route is:

    MARK -> ADMIT -> RETURN -> RECEIPT -> BIND -> VERIFY

The trust rule is:

    No Q, no trust.

## Failure route

Any invalid, unknown, drifted, expired, revoked, unreceipted, unbound, or index-0-positive object must fail closed through:

    REJECTED

A previously verified object may later become:

    REVOKED

Revocation does not delete the receipt.

Revocation denies reliance.

## Positive authority

Only VERIFIED may carry positive reliance under subscriber policy.

BOUND is not enough.

RECEIPTED is not enough.

ADMITTED is not enough.

MARKED is not enough.

Presence is not trust.

## Keeper

Boundary gives the machine an inside.

Language gives the inside a callable action.

State tells us where the action stands.

Receipt proves the call returned.

Verification decides whether reliance is allowed.
