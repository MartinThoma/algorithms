import base64

from fido2.server import Fido2Server
from fido2.webauthn import (
    AuthenticationResponse,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    RegistrationResponse,
)
from flask import Flask, jsonify, request, send_from_directory, session


class RegisteredCredential:
    def __init__(self, credential_id, public_key, sign_count):
        self.credential_id = credential_id
        self.public_key = public_key
        self.sign_count = sign_count


app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"
app.config.update(
    SESSION_COOKIE_SAMESITE="Strict",  # or "None" if cross-origin (with Secure=True)
    SESSION_COOKIE_SECURE=False,  # True only if using HTTPS
)

rp = PublicKeyCredentialRpEntity(name="Example RP", id="localhost")
server = Fido2Server(rp)

# In-memory user store example
users = {}


def to_b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def serialize_webauthn(obj):
    if isinstance(obj, bytes):
        return to_b64url(obj)
    if hasattr(obj, "value"):
        return obj.value
    if hasattr(obj, "__dict__"):
        result = {}
        for key, val in obj.__dict__.items():
            # Skip private/internal attributes if any
            if key.startswith("_"):
                continue
            result[key] = serialize_webauthn(val)
        return result
    if isinstance(obj, (list, tuple)):
        return [serialize_webauthn(i) for i in obj]
    return obj


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def serialize_credential_creation_options(options):
    public_key = options.public_key
    return {
        "publicKey": {
            "challenge": b64url_encode(public_key.challenge),
            "rp": {"name": public_key.rp.name, "id": public_key.rp.id},
            "user": {
                "id": b64url_encode(public_key.user.id),
                "name": public_key.user.name,
                "displayName": public_key.user.display_name,
            },
            "pubKeyCredParams": [
                {"type": p.type.value, "alg": p.alg}
                for p in public_key.pub_key_cred_params
            ],
            "timeout": public_key.timeout or 60000,
            "attestation": public_key.attestation or "none",
            "excludeCredentials": [],  # If you later want to support this
            "authenticatorSelection": {
                "residentKey": public_key.authenticator_selection.resident_key,
                "userVerification": public_key.authenticator_selection.user_verification,
            },
        },
    }


def serialize_auth_options(options) -> dict:
    public_key = options.public_key

    return {
        "challenge": to_b64url(public_key.challenge),
        "timeout": public_key.timeout,
        "rpId": public_key.rp_id,
        "userVerification": public_key.user_verification,
        "allowCredentials": [
            {
                "type": cred.type.value,
                "id": to_b64url(cred.id),
            }
            for cred in public_key.allow_credentials or []
        ],
    }


@app.route("/")
def index():
    return send_from_directory(".", "frontend.html")


@app.route("/register/options", methods=["POST"])
def register_options():
    username = request.json["username"]

    user = PublicKeyCredentialUserEntity(
        id=username.encode("utf-8"),
        name=username,
        display_name=username,
    )

    options, state = server.register_begin(
        user=user,
        credentials=[],
        # resident_key_requirement: How the authenticator handles resident keys.
        # Resident keys are credentials that are stored on the authenticator
        #   "required" if you want to enforce resident keys,
        #   "preferred" if you want to allow but not require them,
        #   "discouraged" if you want to discourage them.
        resident_key_requirement="required",
        # authenticator_attachment: How the authenticator is attached to the device.
        #   "platform" for platform authenticators  (e.g., Touch ID, Face ID, Windows Hello, Android fingerprint)
        #   "cross-platform" for cross-platform authenticators (e.g., YubiKey, USB/Bluetooth/NFC device)
        #   None for any authenticator.
        authenticator_attachment=None,
        # user_verification: How the user proofs their identity to the authenticator.
        #   "required" to require user verification (e.g., PIN, biometric)
        #   "preferred" to prefer user verification but allow without it
        #   "discouraged" to discourage user verification but allow it
        user_verification="required",
    )
    session["state"] = state
    session["username"] = username

    return jsonify(serialize_credential_creation_options(options))


@app.route("/register/complete", methods=["POST"])
def register_complete():
    data = request.json
    state = session.pop("state")
    username = session.get("username")

    raw_id = base64.urlsafe_b64decode(data["rawId"] + "==")
    response = {
        "clientDataJSON": base64.urlsafe_b64decode(
            data["response"]["clientDataJSON"] + "==",
        ),
        "attestationObject": base64.urlsafe_b64decode(
            data["response"]["attestationObject"] + "==",
        ),
    }

    registration_response = RegistrationResponse(
        raw_id=raw_id, response=response
    )

    auth_data = server.register_complete(state, registration_response)
    attested_credential_data = auth_data.credential_data

    users[username] = {
        "credential_id": to_b64url(attested_credential_data.credential_id),
        "public_key": attested_credential_data.public_key,
        "sign_count": auth_data.counter,
    }

    return jsonify({"status": "ok"})


@app.route("/auth/options", methods=["POST"])
def auth_options():
    username = request.json["username"]
    if username not in users:
        return jsonify({"error": "Unknown user"}), 400

    credentials = [
        {
            "id": base64.urlsafe_b64decode(
                users[username]["credential_id"] + "=="
            ),
            "transports": ["usb", "nfc", "ble"],
            "type": "public-key",
        },
    ]

    auth_data, state = server.authenticate_begin(credentials)
    session["state"] = state
    session["username"] = username
    auth_data_serialized = serialize_auth_options(auth_data)
    return jsonify({"publicKey": auth_data_serialized})


@app.route("/auth/complete", methods=["POST"])
def auth_complete():
    data = request.json
    # data looks like this:
    # {
    #     "id": "7rwi3aL3o9f4dq4Zr8soJQ",
    #     "rawId": "7rwi3aL3o9f4dq4Zr8soJQ==",
    #     "type": "public-key",
    #     "response": {
    #         "authenticatorData": "SZYN5YgOjGh0NBcPZHZgW4/krrmihjLHmVzzuoMdl2MZAAAAAA==",
    #         "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uZ2V0IiwiY2hhbGxlbmdlIjoiX1JSUlpBTi1kNThXVHRmN1IyWVVnRVRFeDhvX3g0M3ZKMjY3Z1Ywdm5DdyIsIm9yaWdpbiI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImNyb3NzT3JpZ2luIjpmYWxzZX0=",
    #         "signature": "MEUCIQCQVCGC7d+KwZwJZMGh3prD9aJ83q5/djXNsXZso0QIewIgYHm9zG88MiDbh7j0Z8Dw07P+n55mWRxbAwVXRoDK/Cg=",
    #         "userHandle": "bW9vc2U="
    #     }
    # }

    state = session.pop("state")
    # {'challenge': '05UCoyJGlmksGsQvI-O187oeOVauAZeShj9nf9flZVM', 'user_verification': None}

    def base64url_normalize(s: str) -> str:
        return s + "=" * (-len(s) % 4)

    raw_id = base64url_normalize(data["rawId"])
    data["id"] = raw_id
    data["rawId"] = raw_id

    username = session.get("username")
    if username not in users:
        return jsonify({"error": "Unknown user"}), 400

    auth_response = AuthenticationResponse.from_dict(data)
    credential = RegisteredCredential(
        credential_id=base64.urlsafe_b64decode(data["id"] + "=="),
        public_key=users[username]["public_key"],
        sign_count=users[username]["sign_count"],
    )

    server.authenticate_complete(state, [credential], auth_response)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
