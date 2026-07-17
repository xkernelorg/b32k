# B32K Public Packet Envelope 001

Status: Derived current-repository contract

## Purpose

Every B32K packet may expose the same small, non-secret outer shape. The
shape lets an unfamiliar client or listener recognize B32K, locate the
bootstrap surface, begin a freshness-bound handshake, and carry an otherwise
opaque organizational payload.

Structural validity is not authentication. Authentication is not authority.

## Public envelope

The required fields are:

    b32k
    profile
    handle
    packet_id
    handshake
    payload
    extensions

The recognition value is `b32k: "1"`. The packet profile is
`b32k.packet.public-envelope.001`.

`packet_id` is SHA-256 over canonical UTF-8 JSON containing every envelope
field except `packet_id`. A daemon may separately hash the exact received
bytes as a transport identity. These identities answer different questions:
the canonical ID identifies packet content; the transport ID identifies one
exact serialization.

## Handshake phases

The handshake profile is `b32k.handshake.challenge.001`.

`hello` presents a client nonce and requests a challenge.

`challenge` binds the hello packet, repeats the client nonce, adds a server
nonce and session identifier, and advertises supported authentication
profiles.

`proof` binds both earlier packet identities, both nonces, the session, the
selected authentication profile, and an opaque proof.

A reusable password is never placed in the packet. A future password-based
profile must use a vetted password-authenticated exchange. The current
convention defines transcript shape only; it implements no authentication or
encryption algorithm.

## Payload

A payload declares its visibility as `public`, `mixed`, or `opaque`, and its
encoding as `json`, `b32k-alphabet`, or `opaque`.

Opaque does not automatically mean encrypted. Encryption must be declared by
a future cryptographic profile. Internal labels may remain entirely inside
the payload.

## Boundary

A valid packet may truthfully say:

> I have valid B32K structure. This is my handshake state.

It may not infer:

> I am authenticated, trusted, authorized, or encrypted.

Those claims require later profile verification and organizational admission.
