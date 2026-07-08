# Aletheos Ratification Checklist 001

Status: pre-ratification checklist.

Purpose:

    Define what must be true before the Aletheos binding profile becomes ratified no-redo public law.

Current state:

    B32K public scaffold is live.
    Aletheos binding profile is pre-ratification.
    Aletheos assignments may still be changed by receipt before ratification.
    No sovereign or commercial reliance is allowed yet.

Ratification path:

    draft -> pre-ratification -> ratified

Checklist:

1. Confirm B32K scaffold boundary.
   Aletheos must not alter B32K or claim all possible B32K usage.

2. Confirm root lane.
   Root lane: b32k.aletheos.bound.v1.

3. Confirm Null Well.
   Index 0 = NULL_WELL.
   Index 0 cannot carry positive authority.

4. Confirm Aletheos Root.
   Index 1 = ALETHEOS_ROOT.

5. Confirm operator profile.
   A = local motion.
   M = admission.
   M^T = return.
   Q = receipt.
   Q = M M^T.

6. Decide structural-key assignments.
   Current structural-key assignments are pre-ratification.
   They may be kept, changed, migrated, or discarded before ratification.

7. Confirm canonical index schema.
   The canonical index must enforce lane, index, key, status, authority, and reassignment rules.

8. Confirm validator blocks drift.
   The validator must block duplicate lane/index pairs, illegal positive authority at 0, and mismatched bound entries.

9. Confirm contract language.
   Contract must preserve scaffold/binding distinction, sovereign authority boundary, subscriber reliance boundary, and no-legal-advice status.

10. Confirm no reliance before ratification.
    No commercial or sovereign reliance may be allowed before ratification.

11. Create ratification receipt.
    Only after all required checks pass.

12. Tag release.
    Tag the ratified release only after the ratification receipt is committed.

Keeper:

    The scaffold is live.
    The binding is cooling.
    Ratification is the moment the address becomes promise.
