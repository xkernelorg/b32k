import copy
import hashlib
import json
import re
from dataclasses import dataclass

PACKET_PROFILE = "b32k.packet.public-envelope.001"
HANDSHAKE_PROFILE = "b32k.handshake.challenge.001"
_PACKET_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_HANDLE = re.compile(
    r"^b32k\.[1-9][0-9]*(?:\.[1-9][0-9]*)*$"
)

_TOP_LEVEL_FIELDS = {
    "b32k",
    "profile",
    "handle",
    "packet_id",
    "handshake",
    "payload",
    "extensions",
}
_TOKEN_FIELDS = {"encoding", "value"}
_TOKEN_ENCODINGS = {
    "base64url",
    "b32k-alphabet",
    "opaque",
}
_PAYLOAD_VISIBILITIES = {
    "public",
    "mixed",
    "opaque",
}
_PAYLOAD_ENCODINGS = {
    "json",
    "b32k-alphabet",
    "opaque",
}


class B32KPacketInadmissible(ValueError):
    pass


@dataclass(frozen=True)
class B32KPublicPacket:
    packet_id: str
    handle: str
    handshake_phase: str
    payload_visibility: str
    payload_encoding: str
    record: dict


def canonical_packet_body(record):
    if not isinstance(record, dict):
        raise B32KPacketInadmissible(
            "B32K packet must be an object"
        )
    body = copy.deepcopy(record)
    body.pop("packet_id", None)
    return json.dumps(
        body,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def public_packet_id(record):
    return "sha256:" + hashlib.sha256(
        canonical_packet_body(record)
    ).hexdigest()


def _inspect_token(value, name):
    if not isinstance(value, dict):
        raise B32KPacketInadmissible(
            f"{name} must be an encoded token"
        )
    if set(value) != _TOKEN_FIELDS:
        raise B32KPacketInadmissible(
            f"{name} token shape is invalid"
        )
    if value.get("encoding") not in _TOKEN_ENCODINGS:
        raise B32KPacketInadmissible(
            f"{name} encoding is invalid"
        )
    token = value.get("value")
    if not isinstance(token, str) or len(token) < 16:
        raise B32KPacketInadmissible(
            f"{name} value is too short"
        )


def _inspect_handshake(value):
    if not isinstance(value, dict):
        raise B32KPacketInadmissible(
            "handshake must be an object"
        )
    if "password" in value:
        raise B32KPacketInadmissible(
            "reusable passwords must not be transmitted"
        )
    if value.get("profile") != HANDSHAKE_PROFILE:
        raise B32KPacketInadmissible(
            "handshake profile is invalid"
        )

    phase = value.get("phase")
    required = {
        "hello": {
            "profile",
            "phase",
            "client_nonce",
        },
        "challenge": {
            "profile",
            "phase",
            "hello_packet_id",
            "client_nonce",
            "server_nonce",
            "session_id",
            "authentication_profiles",
        },
        "proof": {
            "profile",
            "phase",
            "hello_packet_id",
            "challenge_packet_id",
            "client_nonce",
            "server_nonce",
            "session_id",
            "authentication_profile",
            "proof",
        },
    }
    if phase not in required or set(value) != required[phase]:
        raise B32KPacketInadmissible(
            "handshake phase shape is invalid"
        )

    _inspect_token(value["client_nonce"], "client_nonce")

    if phase in {"challenge", "proof"}:
        if not _PACKET_ID.fullmatch(value["hello_packet_id"]):
            raise B32KPacketInadmissible(
                "hello_packet_id is invalid"
            )
        _inspect_token(value["server_nonce"], "server_nonce")
        _inspect_token(value["session_id"], "session_id")

    if phase == "challenge":
        profiles = value["authentication_profiles"]
        if (
            not isinstance(profiles, list)
            or not profiles
            or any(
                not isinstance(item, str) or not item
                for item in profiles
            )
            or len(set(profiles)) != len(profiles)
        ):
            raise B32KPacketInadmissible(
                "authentication profiles are invalid"
            )

    if phase == "proof":
        if not _PACKET_ID.fullmatch(
            value["challenge_packet_id"]
        ):
            raise B32KPacketInadmissible(
                "challenge_packet_id is invalid"
            )
        profile = value["authentication_profile"]
        if not isinstance(profile, str) or not profile:
            raise B32KPacketInadmissible(
                "authentication_profile is invalid"
            )
        _inspect_token(value["proof"], "proof")

    return phase


def inspect_public_packet(record):
    if not isinstance(record, dict):
        raise B32KPacketInadmissible(
            "B32K packet must be an object"
        )
    if set(record) != _TOP_LEVEL_FIELDS:
        raise B32KPacketInadmissible(
            "B32K public envelope shape is invalid"
        )
    if record.get("b32k") != "1":
        raise B32KPacketInadmissible(
            "B32K recognition value is invalid"
        )
    if record.get("profile") != PACKET_PROFILE:
        raise B32KPacketInadmissible(
            "B32K packet profile is invalid"
        )

    handle = record.get("handle")
    if not isinstance(handle, str) or not _HANDLE.fullmatch(handle):
        raise B32KPacketInadmissible(
            "B32K destination handle is invalid"
        )

    packet_id = record.get("packet_id")
    if (
        not isinstance(packet_id, str)
        or not _PACKET_ID.fullmatch(packet_id)
        or public_packet_id(record) != packet_id
    ):
        raise B32KPacketInadmissible(
            "B32K packet identity is invalid"
        )

    phase = _inspect_handshake(record.get("handshake"))

    payload = record.get("payload")
    if not isinstance(payload, dict) or set(payload) != {
        "visibility",
        "encoding",
        "content",
    }:
        raise B32KPacketInadmissible(
            "payload shape is invalid"
        )
    if payload["visibility"] not in _PAYLOAD_VISIBILITIES:
        raise B32KPacketInadmissible(
            "payload visibility is invalid"
        )
    if payload["encoding"] not in _PAYLOAD_ENCODINGS:
        raise B32KPacketInadmissible(
            "payload encoding is invalid"
        )
    if not isinstance(payload["content"], (dict, list, str)):
        raise B32KPacketInadmissible(
            "payload content type is invalid"
        )

    if not isinstance(record.get("extensions"), dict):
        raise B32KPacketInadmissible(
            "extensions must be an object"
        )

    return B32KPublicPacket(
        packet_id=packet_id,
        handle=handle,
        handshake_phase=phase,
        payload_visibility=payload["visibility"],
        payload_encoding=payload["encoding"],
        record=copy.deepcopy(record),
    )


def build_public_hello(
    *,
    handle,
    client_nonce,
    payload_visibility="opaque",
    payload_encoding="opaque",
    payload_content="",
    extensions=None,
):
    record = {
        "b32k": "1",
        "profile": PACKET_PROFILE,
        "handle": handle,
        "handshake": {
            "profile": HANDSHAKE_PROFILE,
            "phase": "hello",
            "client_nonce": {
                "encoding": "base64url",
                "value": client_nonce,
            },
        },
        "payload": {
            "visibility": payload_visibility,
            "encoding": payload_encoding,
            "content": copy.deepcopy(payload_content),
        },
        "extensions": copy.deepcopy(extensions or {}),
    }
    record["packet_id"] = public_packet_id(record)
    return inspect_public_packet(record)
