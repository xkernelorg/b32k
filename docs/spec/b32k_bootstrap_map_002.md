# B32K Bootstrap Map 002

Status: Derived current-repository contract

Bootstrap Map 002 supersedes Bootstrap Map 001 while preserving the pinned B32K indexing profile.

    b32k.1          null indexer
    b32k.2          self-referencing B32K bootloader
    b32k.2.1        public B32K orientation shell
    b32k.3          organization root
    b32k.3.1        permanent public organization label
    b32k.3.1.1      organization bootloader
    b32k.3.1.2      public cryptographic disclosure
    b32k.3.2        organization execution surface
    b32k.3.2.1      organization API
    b32k.4          first ordinary lane

## Permanent aliases

    null        b32k.1
    boot        b32k.2
    shell       b32k.2.1
    org         b32k.3
    org.label   b32k.3.1
    org.boot    b32k.3.1.1
    org.crypto  b32k.3.1.2
    org.api     b32k.3.2.1
    lane        b32k.4

Alias resolution is local, deterministic, and non-authoritative. Reserved aliases cannot be overridden, shadowed, or reassigned.

## Mount boundary

The B32K CLI can mount an installed local RookOS CLI:

    b32k mount rookos

Additional arguments are forwarded to `rookos.cli.main`.

Mounting does not install RookOS, authenticate a principal, select a hat, grant a capability, confer authority, or mutate RookOS by itself. Each RookOS command remains subject to its own admission rules.

The current implementation is a local orientation and adapter surface. It does not yet implement public transport, packet ingestion, or cryptographic packet verification.
