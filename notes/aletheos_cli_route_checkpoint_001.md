# Aletheos CLI route checkpoint 001

Timestamp: 2026-07-08T15:36:28

Status: pre-ratification CLI route checkpoint.

This checkpoint records the first live Aletheos CLI route through BIND.

Route:

    :
    MARK
    ADMIT
    RETURN
    RECEIPT
    VERIFY
    BIND

Expected state ladder:

    NULL -> NULL
    NULL -> MARKED
    MARKED -> ADMITTED
    ADMITTED -> RETURNED
    RETURNED -> RECEIPTED
    RECEIPTED -> VERIFIED
    VERIFIED -> BOUND

Route status:

    pass

Final state:

    BOUND

## Boundary

This is Python-hosted.

This is not self-hosting.

This is not ratified.

This assigns no final B32K indices.

This creates no commercial or sovereign reliance.

This is not trust beyond receipt.

## Keeper

The door can be marked, admitted, returned, receipted, verified, and bound.

It still cannot be trusted beyond its receipt.
