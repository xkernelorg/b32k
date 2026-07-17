# Cori Hat Integration Continuity

Status: deferred for later discovery  
Scope: Cori, B32K, `b32kd`, and RookOS boundary  
Current decision: do not invent or imply a Cori hat model

## Purpose

This note preserves the architectural state reached while developing the
B32K-to-RookOS command and HTTP surfaces.

RookOS has an explicit hat model. Cori currently does not. The absence of a
Cori hat model is intentional at this point: no placeholder authority,
implicit role mapping, or convenience alias should be treated as if Cori had
already adopted RookOS hats.

This note exists so that a later maintainer can discover the boundary before
adding Cori execution, cryptographic, research, infrastructure, or governance
services to the B32K public surface.

## Current working stack

The active path is:

    local shell
        -> b32k orientation and mount
        -> RookOS process entry
        -> RookOS authentication and authorization

The local shorthand is:

    ros -> b32k mount rookos --

RookOS rejects direct public process entry when the canonical B32K mount
context is absent. The accepted mount context identifies:

- protocol: `b32k.mount.v1`
- handle: `b32k.3.2.1`
- target: `rookos`

The mount provides orientation only. It does not authenticate a principal,
wear a hat, confer authority, create a mandate, or admit an action.

## Existing RookOS hat support

RookOS currently supports explicit operations for:

- establishing an organizational hat;
- assigning an established hat to a principal;
- selecting or wearing an assigned hat on the local client;
- recording signed establishment and assignment requests;
- retaining xkernel and Xaether evidence references;
- evaluating authority independently from addressability and mounting.

The `trimsetter` hat has been established and assigned in the configured
RookOS organization. Its direct authority list is empty. A separate admitted
domain mandate records its domain powers. Wearing the hat does not create
capabilities that were not independently admitted.

These are RookOS facts. They are not evidence that Cori has hats.

## Current `b32kd` boundary

`b32kd` is a minimal B32K listener with an ephemeral affine spool.

Its responsibilities are limited to:

- exposing public B32K orientation;
- accepting bounded JSON packets;
- preserving exact packet bytes before acknowledgement;
- maintaining recoverable pending delivery state;
- forwarding registered packet actions through the B32K mount;
- hashing returned bytes for response identity;
- completing and safely truncating disposable spool epochs.

The first forwarded action is read-only:

    rookos.organization.show

It invokes exactly:

    b32k mount rookos -- organization show

Packets cannot currently select arbitrary command-line arguments.

The daemon does not:

- interpret organizational policy;
- authenticate or assign hats;
- map Cori identities to RookOS principals;
- confer authority;
- create permanent organizational testimony;
- provide encryption;
- expose mutating RookOS actions;
- define a Cori governance model.

## Cori status

Cori is presently a project and repository family containing research,
authority, protocol, infrastructure, publication, and SDK work.

No reviewed artifact currently establishes:

- a canonical Cori principal model;
- a Cori hat registry;
- a Cori hat lifecycle;
- a Cori authority vocabulary;
- a Cori-to-RookOS principal binding;
- a Cori-to-RookOS hat mapping;
- a Cori mandate admission process;
- a public Cori execution API governed by hats.

Directory names such as `authority`, `governance`, `infrastructure`,
`research`, or `sdk` must not be interpreted as hats or capabilities. A
filesystem location provides organization and discoverability, not authority.

Repository ownership, GitHub access, local shell access, Android process
ownership, and possession of a signing key are also distinct facts. None of
them alone establishes a Cori hat.

## Deferred design question

A future integration may decide that Cori should:

1. adopt RookOS hats directly;
2. define its own role or capability model and bind it to RookOS;
3. remain a collection of projects whose authority is entirely external;
4. expose only public read-only discovery through B32K;
5. combine public discovery with separately authenticated execution lanes.

No option is selected by this note.

The preferred future workflow is discovery before design. Existing Cori
artifacts should be inventoried for actual authority claims, signature
contracts, execution gates, principal references, and durable receipts before
new terminology is introduced.

## Discovery checklist

Before proposing Cori hats, inspect:

- repository-level governance and continuity documents;
- authority and kernel projects;
- Xaether and xkernel bindings;
- cryptographic key ownership and signature namespaces;
- existing principal identifiers;
- service launch and process-custody boundaries;
- public versus private API surfaces;
- any existing mandate, capability, policy, or role vocabulary;
- whether authority is human, service, repository, organization, or
  execution-context scoped;
- whether current artifacts are descriptive, operational, or authoritative;
- whether any claimed action already produces a durable receipt.

The discovery report should distinguish:

- identity from authentication;
- authentication from authorization;
- authorization from execution;
- execution from testimony;
- repository access from organizational authority;
- B32K addressability from RookOS admission;
- a public label from a privileged API;
- local process custody from cryptographic trust.

## Requirements for any future mapping

If a Cori-to-RookOS hat mapping is later proposed, it should be explicit,
versioned, testable, and fail closed.

At minimum, it should identify:

- the Cori subject being represented;
- the canonical RookOS organization;
- the principal receiving or exercising the hat;
- the hat identifier and lifecycle state;
- the exact authority vocabulary;
- the source artifact authorizing the mapping;
- authentication requirements;
- request and signature namespaces;
- pre-state binding;
- admission and idempotency rules;
- xkernel or other execution evidence;
- permanent receipt behavior;
- revocation or supersession behavior;
- public disclosure and privacy boundaries.

The mapping must not be inferred from a B32K handle, daemon packet, Git
remote, directory name, shell alias, or successful mount.

## Encryption continuity

The current stack uses SHA-256 content identities and SSH signatures, but no
application-level encryption service is active in the B32K, `b32kd`, or
RookOS packet path.

OpenFHE tooling exists elsewhere in Cori infrastructure, but it is not
currently mounted as an active encryption service and does not protect
`b32kd` HTTP transport or spool storage.

Any future encrypted Cori service should separately disclose:

- transport encryption;
- encryption at rest;
- payload or field encryption;
- key custody;
- algorithm and parameter profiles;
- implementation and library versions;
- authentication relationship;
- failure and downgrade behavior;
- whether encryption changes visibility only or also participates in policy.

Encryption must not be confused with hats or authority.

## Nonclaims

This note does not claim that:

- Cori has hats;
- Cori lacks all authority structures;
- RookOS authority automatically governs every Cori project;
- mounting RookOS authenticates a caller;
- `b32kd` is an authorization service;
- a SHA-256 digest is authentication or encryption;
- a successful read-only request creates a permanent record;
- the current architecture is final.

## Continuity instruction

Leave this note in the B32K repository until Cori authority discovery is
performed.

When that discovery occurs:

1. cite the concrete Cori artifacts inspected;
2. record what authority model actually exists;
3. decide whether hats are adopted, mapped, or rejected;
4. preserve the separation between B32K orientation, daemon transport, and
   RookOS authorization;
5. add tests before exposing any mutating action through `b32kd`;
6. supersede this note explicitly rather than silently deleting its boundary.

Until then, Cori has no declared hat surface, and `b32kd` must not invent one.
