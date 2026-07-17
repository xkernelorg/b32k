# B32K Address Space Convention 001

Status: Derived current-repository contract

B32K has 32768 finite registered catalogue positions. Those positions are canonical entry points, not the full universe of descendant objects.

Successor boundary:

    actual null: outside the registry
    catalogue 1 / registered index 0: NULL_WELL
    catalogue 2 / registered index 1: B32K_BOOTLOADER
    catalogue 3 / registered index 2: ORGANIZATION_ROOT
    catalogue 4..32768 / registered indices 3..32767: ordinary positions

A lane or context descending from a registered position may be unbounded.

Nonclaims: addressability does not confer authority; unsigned addressability does not confer trust; an entry point does not exhaust its descendant lane or context.
