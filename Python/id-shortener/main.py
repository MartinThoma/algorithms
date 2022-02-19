import uuid
import binascii

ident = uuid.uuid4()
bytestring = ident.bytes

encodings = [
    ("uu", binascii.b2a_uu),
    ("base64", binascii.b2a_base64),
    ("qp", binascii.b2a_qp),
    ("hex", binascii.b2a_hex),
    ("hqx", binascii.b2a_hqx),
]

for name, func in encodings:
    print(f"{name:<20}: {func(bytestring)}")
