# from pydantic import BaseModel

# class Transaction(BaseModel):
#     version_number: str  # 4 Byte

#     # How many UTXOs are consumed?
#     input_counter: int

#     tx_out_hash : str
#     tx_out_index : int
#     input_script: str
#     sequence: str
#     output_script: str
#     pub_key_length: int


def reorder(hex_chars: str) -> str:
    hex_chars = list(hex_chars[::-1])
    for i in range(len(hex_chars) // 2):
        hex_chars[2*i], hex_chars[2*i + 1] = hex_chars[2*i+1], hex_chars[2*i]
    return "".join(hex_chars)

def hex_to_num(hex_chars: str) -> int:
    return int(reorder(hex_chars), 16)

def disect_transaction(tx: str) -> "Transaction":
    """

    1 hex character can encode 16 values
    1 Byte has 8 Bit and thus 2**8 = 256 values
    2 hex characters can encode 16**2 = 256 values
    Hence: 2 hex chars = 1 Byte
    """
    byte = 2

    char_current = 0
    char_next = char_current + 4*byte
    version_number = hex_to_num(tx[char_current:char_next])
    print(f"{version_number=}")

    char_current = char_next
    char_next = char_current + 1*byte
    input_counter = tx[char_current:char_next]
    print(f"{input_counter=}")

    char_current = char_next
    char_next = char_current + 32*byte
    tx_out_hash = tx[char_current:char_next]
    print(f"{tx_out_hash=}")

    char_current = char_next
    char_next = char_current + 4*byte
    tx_out_index = tx[char_current:char_next]
    print(f"{tx_out_index=}")

    char_current = char_next
    char_next = char_current + 2*byte
    unclear = hex_to_num(tx[char_current:char_next])
    print(f"{unclear=}")

    char_current = char_next
    char_next = char_current + 1*byte
    input_script_length = hex_to_num(tx[char_current:char_next])
    print(f"{input_script_length=}")

    char_current = char_next
    char_next = char_current + input_script_length*byte
    input_script = tx[char_current:char_next]
    print(f"{input_script=}")

    char_current = char_next
    char_next = char_current + 4*byte
    sequence = hex_to_num(tx[char_current:char_next])
    print(f"{sequence=}")  # What is this sequence number used for?

    char_current = char_next
    char_next = char_current + 1*byte
    nb_out = hex_to_num(tx[char_current:char_next])
    print(f"{nb_out=}")

    print("## Output follows " + "#" * 60)
    for out_index in range(nb_out):
        char_current = char_next
        char_next = char_current + 4*byte
        value = hex_to_num(tx[char_current:char_next])
        print(f"{value=}")

        char_current = char_next
        char_next = char_current + 4*byte
        unclear = tx[char_current:char_next]
        print(f"{unclear=}")

        char_current = char_next
        char_next = char_current + 1*byte
        out_script_length = hex_to_num(tx[char_current:char_next])

        char_current = char_next
        char_next = char_current + out_script_length*byte
        out_script = tx[char_current:char_next]
        print(f"{out_script=}")
        print("-"*80)
    print("#" * 80)

    char_current = char_next
    char_next = char_current + 1*byte
    unclear = hex_to_num(tx[char_current:char_next])
    print(f"{unclear=}")

    char_current = char_next
    char_next = char_current + 1*byte
    unclear = hex_to_num(tx[char_current:char_next])
    print(f"{unclear=}")

    char_current = char_next
    print(f"Rest: {tx[char_current:]} (length: {len(tx[char_current:])} chars)")


# https://blockchain.info/tx/30713d08afa548d3465e380d6e1837354b29a1b6707e2a913b27776cf305fda4?format=json
# tx = disect_transaction("010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff5403df550a1b4d696e656420627920416e74506f6f6c373138fd004702c13ba070fabe6d6d6d9986fd3aedb9f8b00fab3c74c2e1d399fd0e6bc1d964aa57a08f78ac2d648002000000000000001eb50000c1377c00ffffffff04653c3a2a000000001976a91411dbe48cc6b617f9c6adaf4d9ed5f625b1c7cb5988ac0000000000000000266a24aa21a9ede0721e21cc17367eb4fcccf94c7e6ebc54757a693515f809307d4d6a31e0c8500000000000000000266a24b9e11b6d6eab9aaf2ccdc3cb05fb15989c512b84c8ef5f498559cd4d66e6104de8f9cdb100000000000000002b6a2952534b424c4f434b3a93320d7a461a95b953bd18e40aa031b5470d6258ccd82011999a5b290031529c0120000000000000000000000000000000000000000000000000000000000000000000000000")

# https://blockchain.info/tx/5199467818921262400267588408f481ab30db455eef700bd965fab9bfa10dec?format=hex
tx = disect_transaction("010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff64039d560a2cfabe6d6d0d5545b446f0e9c35bb42c6fec8c9a6c3ef4b6f64d9a01e2169f01dc5a77d50f10000000f09f909f082f4632506f6f6c2f104d696e656420627920626967686f726e00000000000000000000000000000000000000050022e600000000000004a4858c27000000001976a914c825a1ecf2a6830c4401620c3a16f1995057c2ab88ac0000000000000000266a24aa21a9ed8630f428a357cf72ae52cd6f78d3e1156a6496682e54fee6fc6bc8ccb8a1d6e900000000000000002c6a4c2952534b424c4f434b3a23a972ed54a376c793d6ccd71eb3952535b81e8c040392c426da052d003160ee0000000000000000266a24b9e11b6d03a83f229005077a5c750dc9f3944de70ba59c0ac9874d2eb97770c25e60a27001200000000000000000000000000000000000000000000000000000000000000000a8c91d3f")