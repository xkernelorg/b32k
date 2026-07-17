# B32K Indexing Profile 002

Status: Derived current-repository contract

Supersedes: `b32k_indexing_profile_001`

## Purpose

This profile distinguishes the global B32K bootstrap boundary from
Aletheos-bound lane terminology.

## Boot sequence

The first three wire or lane positions are interpreted as follows:

    index 0  NULL_WELL
    index 1  B32K_BOOTLOADER
    index 2  first user-space allocation

Their one-based catalogue addresses are:

    address 1  NULL_WELL
    address 2  B32K_BOOTLOADER
    address 3  first user-space allocation

Catalogue address 0 remains outside the registry.

## Registered null

Catalogue address 1 maps to wire index 0. It is an explicit registered
null and carries no positive authority.

## B32K bootloader

Catalogue address 2 maps to wire index 1. This position anchors B32K
itself and is not available for user-space reassignment.

## User space

User allocation begins at catalogue address 3, wire or lane index 2,
and continues through catalogue address 32768, index 32767.

A Rook organization may therefore use index 2 as its organization
root while retaining the rest of the lane for organizational objects.

## Aletheos boundary

Existing Aletheos documents describing `ALETHEOS_ROOT` at lane index 1
are Aletheos-bound, pre-ratification lane documents. They do not assign
the global B32K bootstrap position to Aletheos and do not change the
B32K boot sequence defined here.

## Preservation rule

Existing content hashes remain primary identities. A B32K address is a
typed secondary coordinate. Address assignment does not confer
authority, prove truth, or rewrite historical receipts.
