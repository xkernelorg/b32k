# B32K Indexing Profile 001

Status: Derived current-repository contract

## Purpose

This profile resolves the indexing conventions presently carried by the
canonical alphabet, codec, and Aletheos-bound index artifacts.

## Coordinate systems

B32K uses three related coordinates.

- Catalogue address: 1 through 32768.
- Wire index: 0 through 32767.
- Lane index: 0 through 32767 within a named lane.

The conversion is exact:

    wire_index = catalogue_address - 1
    catalogue_address = wire_index + 1

Catalogue address 0 is outside the registry.

## Registered null

Catalogue address 1 maps to wire index 0 and lane index 0.

In the Aletheos-bound lane this position is NULL_WELL. It is an
explicit registered null, carries no positive authority, and must not
be confused with a missing field or an address outside the registry.

## Aletheos root

Catalogue address 2 maps to wire index 1 and lane index 1.

In the Aletheos-bound lane this position is ALETHEOS_ROOT.

## Final address

Catalogue address 32768 maps to wire index 32767. The wire value
therefore remains representable in exactly fifteen bits.

## Preservation rule

Existing canonical alphabet addresses remain one-based. Existing codec
and lane indices remain zero-based. Neither surface is renumbered.

Definitions may mature, but admitted addresses must not drift.

## Nonclaims

A glyph does not confer authority. A semantic definition does not
change an address. A wire index is not itself a catalogue address.
