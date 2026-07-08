# Aletheos Operator Profile 001

Status: pre-ratification technical profile.

## Purpose

This profile defines the primary operator discipline for B32K bound to Aletheos.

It does not alter the public B32K scaffold.

It defines how Aletheos treats motion, admission, return, and receipt inside declared Aletheos lanes.

## Operator roles

A is the local motion operator.

M is the admission operator.

M^T is the return operator.

Q is the receipt operator.

The primary receipt law is:

    Q = M M^T

This means that an Aletheos-bound object is not trusted merely because it is present. It must pass through admission and return as a reproducible receipt.

## Reference Thalean identity

In the Thalean reference core, where A is the adjacency operator of G15 isomorphic to L(Petersen), the receipt operator satisfies:

    Q = M M^T = A^3 + 2A^2 + 2I

This identity is the reference witness for the operator discipline.

It is not a claim that every B32K use must literally realize the Thalean core.

It is the canonical example showing how local motion, incidence admission, and receipt overlap can close into an exact finite law.

## CPU-from-null reading

The minimal Aletheos apparatus reads:

    0 Null Well
    1 Mark
    2 Logic
    3 Language
    4 Sequence
    5 Memory
    6 I/O
    7 Receipt

The operator chain is:

    input -> language -> logic -> admission M -> return M^T -> receipt Q

## Commercial trust reading

A certificate is not valid merely because it exists.

It must enter an admission register M.

It must return through a verification relation M^T.

It must produce a receipt Q.

No Q, no trust.

## Keeper

A is local motion.

M is admission.

M^T is return.

Q is receipt.

Aletheos does not trust presence.

Aletheos trusts admitted return.
