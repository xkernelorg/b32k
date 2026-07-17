# B32K Bootstrap Map 001

Status: Derived current-repository contract

B32K exposes a stable hierarchical bootstrap map.

    b32k.1          null indexer
    b32k.2          self-referencing B32K bootloader
    b32k.2.1        public B32K shell
    b32k.3          organization root
    b32k.3.1.1      organization bootloader
    b32k.3.1.2      organization API
    b32k.4          first ordinary lane

The top-level segment names a finite registered catalogue position. Segments after that position name descendant lane or context paths. Descendant paths do not consume additional positions in the finite catalogue.

## Universal bootstrap law

A packet claimed as B32K may enter through `b32k.2.1`.

The B32K bootloader verifies the packet envelope and pinned profile, preserves packet identity, and issues a bootstrap receipt.

Its sole external action is:

    pipe the verified packet unchanged to b32k.3.1.1

The global bootloader may not interpret organizational authority, allocate an ordinary lane, invoke the organization API, or mutate the packet.

## Organization boundary

The packet binding supplies the organization identity represented by `b32k.3`.

The organization bootloader is available at `b32k.3.1.1`. It may resolve or advertise the organization API at `b32k.3.1.2`.

Discovery of the API does not confer authority. Authentication and admission remain inside the organization boundary.

## Nonclaims

Public shell access does not confer trust or authority. Addressability does not replace identity. The bootstrap map does not claim a network transport, executable shell implementation, or public deployment.
