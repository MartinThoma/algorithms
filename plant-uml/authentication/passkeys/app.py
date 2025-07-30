import base64

from fido2.server import Fido2Server
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    RegistrationResponse,
)
from flask import Flask, jsonify, request, send_from_directory, session

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
        user_verification="preferred",
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

    registration_response = RegistrationResponse(raw_id=raw_id, response=response)

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
            "id": base64.urlsafe_b64decode(users[username]["credential_id"] + "=="),
            "transports": ["usb", "nfc", "ble"],
            "type": "public-key",
        },
    ]

    auth_data, state = server.authenticate_begin(credentials)
    session["state"] = state
    session["username"] = username
    auth_data_serialized = serialize_auth_options(auth_data)
    return jsonify(auth_data_serialized)


@app.route("/auth/complete", methods=["POST"])
def auth_complete():
    data = request.json
    client_data = data["clientDataJSON"]
    authenticator_data = data["authenticatorData"]
    signature = data["signature"]
    credential_id = data["id"]

    state = session.pop("state")
    username = session.get("username")
    if username not in users:
        return jsonify({"error": "Unknown user"}), 400

    credential = users[username]
    server.authenticate_complete(
        state,
        [credential],
        credential_id,
        client_data,
        authenticator_data,
        signature,
    )
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
