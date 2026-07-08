# B32K-Aletheos Sovereign Trust Registry Agreement

Draft 003

Status: Conceptual and technical contract scaffold. Not final legal advice. Requires legal review before public-sector, sovereign, regulated, or commercial deployment.

## 1. Purpose

This Agreement defines the terms under which B32K may be used as a symbolic scaffold for Aletheos-bound semantic registries, sovereign trust lanes, certificate issuance, subscriber verification, and receipt-ledger accountability.

The Agreement does not claim that B32K belongs to Aletheos.

The Agreement does not claim that Aletheos governs all possible B32K use.

The Agreement defines one governed binding profile:

    B32K bound to Aletheos

A Subscriber may declare:

    We use B32K bound to Aletheos.

A sovereign or institutional participant may further declare:

    We issue or accept certificates under a declared Aletheos sovereign lane.

## 2. Core roles

B32K is the symbolic scaffold. It provides the canonical address space, symbol indices, encoding rules, and transportable substrate.

Aletheos is the semantic binding profile over B32K. It defines how B32K indices become witnessed semantic addresses inside declared Aletheos lanes.

A Sovereign Authority is a government, nation, public authority, treaty authority, institution, or authorized registry body that issues or governs trust certificates under a declared sovereign lane.

A Subscriber is a person, organization, system, agent, device, or network that elects to rely on certificates, bindings, or receipts issued under one or more declared lanes.

A Verifier is a party or system that checks certificate validity, receipt history, issuer authority, revocation state, schema conformance, lane scope, and canonical payload integrity.

A Xaether-compatible system accepts B32K symbols only when their semantic binding and receipt chain resolve through a declared Aletheos lane.

## 3. Scoping principle

B32K is the symbolic scaffold.

Aletheos defines a binding profile over that scaffold.

No Aletheos binding shall be interpreted as a claim over all possible B32K usage.

Aletheos-bound objects are valid only within declared Aletheos lanes, schemas, receipts, authority boundaries, and subscriber policies.

Other uses of B32K may exist outside Aletheos, including private lanes, experimental lanes, raw codec usage, package registries, and non-Aletheos semantic systems.

Keeper:

    B32K is the scaffold.
    Aletheos is the declared way of climbing it.

## 4. Root lane and root address

The Aletheos root binding lane is:

    b32k.aletheos.bound.v1

Within that lane:

    index 0 = Null Well
    index 1 = Aletheos Root

Index 1 denotes the first admitted witness root from which Aletheos-bound semantic, sovereign, certificate, subscriber, structural-key, and receipt lanes descend.

Everything Aletheos defines branches from index 1 within declared Aletheos lanes.

The rest of B32K remains open for other lawful, private, experimental, sovereign, institutional, or non-Aletheos assignment systems.

## 5. Null Well reservation

Within every Aletheos-bound B32K lane, index 0 is permanently reserved as the Null Well address.

Index 0 is not Aletheos.

Index 0 is not a sovereign authority.

Index 0 is not a certificate class.

Index 0 is not a structural key.

Index 0 is not a subscriber.

Index 0 is not a positive claim.

Index 0 denotes the unbound socket against which positive bindings stand.

Index 0 may represent null, unbound, pre-admission, withheld, failed binding, non-claim, or explicit absence of authority.

Any certificate, claim, lane, issuer, subscriber declaration, trust object, or registry object that relies on index 0 as positive authority MUST be rejected.

Keeper:

    Zero is the well.
    One is the witness root.

## 6. Aletheos crossing

Aletheos begins where null is refused as authority.

An object crosses into Aletheos-bound status only when it satisfies required normalization and witness conditions:

- canonical encoding
- declared lane
- valid nonzero B32K index
- valid structural key or certificate type
- schema conformance
- receipt generation
- verification policy
- authority boundary declaration

Aletheos is the witness boundary that proves the symbol did not remain in the Null Well.

Keeper:

    Aletheos is not zero.
    Zero is the well.
    Aletheos is the crossing that proves the symbol did not remain there.

## 7. Normalization ladder

The Registry recognizes the following normalization ladder as a design constraint:

0. Null Well. No admitted binding. No positive claim. No authority.

1. Mark. A first positive address or symbol exists.

2. Relation. The mark is bound across a declared relation.

3. Chamber. The relation is scoped inside a lane, schema, jurisdiction, institution, or authority domain.

4. Closure. The scoped relation becomes checkable, signed, receipted, or otherwise closed under verification.

5. Body. The closed object carries admitted content, such as a certificate, claim, structural key, identity assertion, trust object, or sovereign registry entry.

This ladder is not numerology. It is a normalization grammar for preventing null, mark, relation, authority, and receipt from collapsing into one another.

Keeper:

    Zero is the well.
    One is the first admitted mark.
    Two is relation.
    Three is chamber.
    Four is closure.
    Five is body.

## 8. Lane structure

The Aletheos root semantic lane is:

    b32k.aletheos.bound.v1

A sovereign lane may be declared beneath it, for example:

    b32k.aletheos.sovereign.ca.v1

A certificate lane may be declared beneath a sovereign lane, for example:

    b32k.aletheos.sovereign.ca.trust_certificate.v1

Other possible subordinate lanes include:

    b32k.aletheos.sovereign.ca.identity.v1
    b32k.aletheos.sovereign.ca.origin.v1
    b32k.aletheos.sovereign.ca.compliance.v1
    b32k.aletheos.sovereign.ca.revocation.v1

A lane must be declared before certificates or trust objects may be issued under it.

A lane declaration must specify lane_id, parent_lane, authority_scope, allowed object classes, issuer policy, schema references, revocation policy, subscriber reliance policy, version, canonical index rules, Null Well reservation, and Aletheos root relationship.

## 9. Canonical index rule

A canonical index records B32K address assignments within a declared lane.

Once a B32K index is assigned within a canonical Aletheos-bound lane, the assignment must not silently change.

Definitions may mature. Aliases may be added. Certificates may expire. Certificates may be revoked. Authorities may rotate keys. Subscribers may change trust policy. Lanes may version.

But issued addresses and receipts must not silently drift.

A correction must be recorded as a new version, alias, deprecation, revocation, supersession, corrective receipt, or new lane.

No object may reuse an already assigned index inside the same lane unless the canonical index explicitly defines it as an alias or supersession relationship.

## 10. Certificate structure

A trust certificate should include, at minimum:

- certificate_id
- certificate_type
- encoding
- binding_authority
- binding_lane
- sovereign_authority
- sovereign_lane
- certificate_lane
- issuer
- subject
- claim
- scope
- issued_at
- expires_at
- status
- revocation_status
- canonical_payload_hash
- receipt
- signature
- verification_uri

Example:

    encoding: B32K
    binding_authority: Aletheos
    binding_lane: b32k.aletheos.bound.v1
    sovereign_authority: Canada
    sovereign_lane: b32k.aletheos.sovereign.ca.v1
    certificate_lane: b32k.aletheos.sovereign.ca.trust_certificate.v1
    certificate_type: trust_certificate

## 11. Sovereign authority

A Sovereign Authority may issue trust certificates only after the certificate has crossed the full normalization ladder:

- source payload exists
- payload canonicalizes
- payload is assigned to a nonzero B32K address
- payload is bound through the Aletheos lane
- payload is scoped to a sovereign lane
- issuer authority is valid
- certificate schema validates
- receipt is generated
- status is recorded
- verification policy is available

A sovereign certificate is not valid merely because it exists in storage.

It is valid only when it is normalized, witnessed, authorized, receipted, and not revoked.

Aletheos does not certify the legal truth of a sovereign claim unless expressly authorized to do so.

Aletheos certifies the binding, schema, receipt, index state, and verification surface.

The Sovereign Authority certifies the legal or institutional claim.

## 12. Issuance

A certificate may be issued only if the certificate lane exists, the issuer is authorized, the schema is valid, the payload canonicalizes successfully, the object uses a valid nonzero B32K index, the object is bound through Aletheos, the certificate is signed by an approved key, the certificate receives a deterministic receipt, and the certificate status is recorded in the registry.

Issuance does not imply universal trust.

Issuance means the certificate was validly created under the declared lane, issuer, schema, and authority boundary.

## 13. Verification

A Verifier may verify:

- certificate payload integrity
- valid nonzero B32K address
- declared Aletheos lane
- declared sovereign lane
- declared certificate lane
- issuer key validity at issuance
- certificate schema validity
- expiration state
- revocation state
- receipt history consistency
- canonical payload hash match

Verification must be deterministic.

A verifier should be able to reproduce the certificate hash and confirm registry status without altering the registry.

## 14. Subscriber reliance

A Subscriber may declare:

    We use B32K bound to Aletheos.

A Subscriber may further declare:

    We accept certificates issued under b32k.aletheos.sovereign.ca.trust_certificate.v1.

Subscriber reliance may be limited by certificate type, issuer, jurisdiction, time period, risk class, claim type, subscriber policy, or verification policy.

A Subscriber MUST NOT rely on index 0, unbound objects, unreceipted payloads, expired certificates, revoked certificates, unknown lanes, unknown issuers, or objects whose canonical payload has drifted from its receipt.

## 15. Xaether compatibility

Xaether-compatible systems may declare:

    encoding: B32K
    binding: Aletheos
    accepted_lane: b32k.aletheos.bound.v1
    accepted_sovereign_lane: b32k.aletheos.sovereign.ca.v1

Such a declaration means the system accepts B32K symbols only when their semantic binding and receipt chain resolve through the declared Aletheos lane.

Xaether-compatible systems MAY reject any certificate, claim, action, or trust object that attempts to treat index 0 as authority.

Keeper:

    B32K gives the symbol an address.
    Aletheos gives the address a witness.
    A sovereign gives the witness authority.
    Xaether accepts the authority through a declared binding.

## 16. Privacy and disclosure

A certificate may publish only a digest, handle, or receipt when the underlying payload is private.

Public registry entries should minimize personal or sensitive data.

Private certificate payloads may be disclosed only according to the issuing authority's policy and applicable law.

Digest-only public anchoring may be used where payload disclosure is not permitted.

## 17. Revocation and supersession

A certificate may be revoked, suspended, expired, or superseded.

Revocation must not delete the original certificate receipt.

Supersession must point from the old certificate to the new certificate.

The registry must preserve issuance, verification, revocation, supersession, issuer key changes, schema changes, lane version changes, and subscriber policy changes where applicable.

## 18. Data integrity

All registry objects must be canonicalized before hashing, signing, receipting, anchoring, or verifying.

A non-canonical object is not registry-valid.

Any implementation that changes field order, encoding, normalization, lane identity, index assignment, payload hash, or receipt state in a way that changes the canonical payload must treat the result as a new object.

## 19. Governance

The Aletheos Registry Operator maintains Aletheos root lane definitions, Null Well reservation, canonical index rules, schema registry, receipt format, verification rules, implementation conformance tests, and the Aletheos binding profile.

The Sovereign Authority maintains issuer authorization, certificate policy, legal scope, revocation authority, subscriber-facing trust rules, and jurisdictional compliance.

The Subscriber maintains accepted lanes, accepted issuers, accepted certificate types, reliance policy, and verification requirements.

## 20. Warranties and reliance

The registry proves binding, receipt, and integrity.

It does not automatically prove the worldly truth of every claim.

Reliance on a certificate is governed by certificate type, issuer authority, subscriber policy, sovereign law, applicable regulation, and verification status.

## 21. Versioning

A lane version may be updated only by creating a new versioned lane.

Existing certificates remain bound to the lane version under which they were issued.

A future lane may supersede an earlier lane, but must not erase it.

Index assignments and receipts from earlier lanes remain part of the historical ledger.

## 22. Keeper clauses

B32K is the scaffold.

Aletheos is the declared way of climbing it.

Zero is the well.

One is the witness root.

Aletheos does not consume B32K.

Aletheos roots a witness lane inside B32K.

Everything Aletheos-bound descends from 1.

Zero remains the well.

Definitions may mature.

Certificates may expire.

Authorities may revoke.

Lanes may version.

Addresses and receipts must not silently drift.

B32K gives the symbol an address.

Aletheos gives the address a witness.

A sovereign gives the witness authority.

Xaether accepts the authority through a declared binding.

## 23. Draft status

This draft is a conceptual and technical scaffold.

It is not final legal advice.

Before use with a sovereign authority, public institution, regulated industry, commercial subscriber, or public certificate registry, this Agreement should be reviewed by counsel familiar with digital identity, public-sector procurement, cryptographic signatures, certificate authority governance, privacy law, administrative law, Indigenous and sovereign registry law where applicable, and cross-border data governance.

## LLM viewer boundary

B32K is aetherial first.

A language model is not the B32K kernel.

A language model may act as a viewer, narrator, proposer, translator, or interface for B32K and Aletheos-bound materials.

A language model may not become the source of canonical authority, final index assignment, ratification, receipt, verification, or sovereign reliance.

B32K and Aletheos-bound materials must be built as if no language model exists, while remaining legible enough for language models to view and explain truthfully.

Language-model outputs are advisory until admitted by the Aletheos apparatus.

A language model may MARK or propose, but Aletheos must ADMIT, RETURN, RECEIPT, VERIFY, BIND, REJECT, or REVOKE according to declared artifacts and receipts.

Model confidence is not authority.

Embedding similarity is not provenance.

Generated text is not ratification.

The LLM may view the aether. It may not become the aether.

