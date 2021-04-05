from pydantic import BaseModel  # pip install pydantic
from typing import List, Tuple
from binascii import unhexlify, hexlify


class TxIn(BaseModel):
    tx_id: str
    tx_index: int
    script: str
    sequence: int


class TxOut(BaseModel):
    satoshi: int
    script: str


class Witness(BaseModel):
    stack_items: List[List[str]]


class Transaction(BaseModel):
    version_number: int
    marker: str
    flag: str
    tx_ins: List[TxIn]
    tx_outs: List[TxOut]
    witness: Witness

    # Is this a unix timestamp or a block number?
    # It encodes when the
    locktime: int


def reorder(hex_chars: str) -> str:
    hex_chars = list(hex_chars[::-1])
    for i in range(len(hex_chars) // 2):
        hex_chars[2 * i], hex_chars[2 * i + 1] = hex_chars[2 * i + 1], hex_chars[2 * i]
    return "".join(hex_chars)


def hex_to_num(hex_chars: str) -> int:
    return int(reorder(hex_chars), 16)


def bytes_to_asm(byte_stream: bytes) -> List[str]:
    # Verify with https://btc.com/tools/tx/decode
    # continue with the rest of opcodes, grab from https://github.com/bcoin-org/bcoin/blob/master/lib/script/common.js
    # https://github.com/rust-bitcoin/rust-bitcoin/blob/master/src/blockdata/opcodes.rs
    opcodes = {
        # Push
        0x00: "OP_0",
        0x4C: "OP_PUSHDATA1",
        0x4D: "OP_PUSHDATA2",
        0x4E: "OP_PUSHDATA4",
        0x4F: "OP_1NEGATE",
        0x50: "OP_RESERVED",
        0x51: "OP_1",
        0x52: "OP_2",
        0x53: "OP_3",
        0x54: "OP_4",
        0x55: "OP_5",
        0x56: "OP_6",
        0x57: "OP_7",
        0x58: "OP_8",
        0x59: "OP_9",
        0x5A: "OP_10",
        0x5B: "OP_11",
        0x5C: "OP_12",
        0x5D: "OP_13",
        0x5E: "OP_14",
        0x5F: "OP_15",
        0x60: "OP_16",
        # Control
        0x61: "OP_NOP",
        0x62: "OP_VER",
        0x63: "OP_IF",
        0x64: "OP_NOTIF",
        0x65: "OP_VERIF",
        0x66: "OP_VERNOTIF",
        0x67: "OP_ELSE",
        0x68: "OP_ENDIF",
        0x69: "OP_VERIFY",
        0x6A: "OP_RETURN",
        # Stack
        0x6B: "OP_TOALTSTACK",
        0x6C: "OP_FROMALTSTACK",
        0x6D: "OP_2DROP",
        0x6E: "OP_2DUP",
        0x6F: "OP_3DUP",
        0x70: "OP_2OVER",
        0x71: "OP_2ROT",
        0x72: "OP_2SWAP",
        0x73: "OP_IFDUP",
        0x74: "OP_DEPTH",
        0x75: "OP_DROP",
        0x76: "OP_DUP",
        0x77: "OP_NIP",
        0x78: "OP_OVER",
        0x79: "OP_PICK",
        0x7A: "OP_ROLL",
        0x7B: "OP_ROT",
        0x7C: "OP_SWAP",
        0x7D: "OP_TUCK",
        # Splice
        0x7E: "OP_CAT",
        0x7F: "OP_SUBSTR",
        0x80: "OP_LEFT",
        0x81: "OP_RIGHT",
        0x82: "OP_SIZE",
        # Bit
        0x83: "OP_INVERT",
        0x84: "OP_AND",
        0x85: "OP_OR",
        0x86: "OP_XOR",
        0x87: "OP_EQUAL",
        0x88: "OP_EQUALVERIFY",
        0x89: "OP_RESERVED1",
        0x8A: "OP_RESERVED2",
        # Numeric
        0x8B: "OP_1ADD",
        0x8C: "OP_1SUB",
        0x8D: "OP_2MUL",
        0x8E: "OP_2DIV",
        0x8F: "OP_NEGATE",
        0x90: "OP_ABS",
        0x91: "OP_NOT",
        0x92: "OP_0NOTEQUAL",
        0x93: "OP_ADD",
        0x94: "OP_SUB",
        0x95: "OP_MUL",
        0x96: "OP_DIV",
        0x97: "OP_MOD",
        0x98: "OP_LSHIFT",
        0x99: "OP_RSHIFT",
        0x9A: "OP_BOOLAND",
        0x9B: "OP_BOOLOR",
        0x9C: "OP_NUMEQUAL",
        0x9D: "OP_NUMEQUALVERIFY",
        0x9E: "OP_NUMNOTEQUAL",
        0x9F: "OP_LESSTHAN",
        0xA0: "OP_GREATERTHAN",
        0xA1: "OP_LESSTHANOREQUAL",
        0xA2: "OP_GREATERTHANOREQUAL",
        0xA3: "OP_MIN",
        0xA4: "OP_MAX",
        0xA5: "OP_WITHIN",
        # Crypto
        0xA6: "OP_RIPEMD160",
        0xA7: "OP_SHA1",
        0xA8: "OP_SHA256",
        0xA9: "OP_HASH160",
        0xAA: "OP_HASH256",
        0xAB: "OP_CODESEPARATOR",
        0xAC: "OP_CHECKSIG",
        0xAD: "OP_CHECKSIGVERIFY",
        0xAE: "OP_CHECKMULTISIG",
        0xAF: "OP_CHECKMULTISIGVERIFY",
        # Expansion
        0xB0: "OP_NOP1",
        0xB1: "OP_CHECKLOCKTIMEVERIFY",
        0xB2: "OP_CHECKSEQUENCEVERIFY",
        0xB3: "OP_NOP4",
        0xB4: "OP_NOP5",
        0xB5: "OP_NOP6",
        0xB6: "OP_NOP7",
        0xB7: "OP_NOP8",
        0xB8: "OP_NOP9",
        0xB9: "OP_NOP10",
        # Every other opcode acts as OP_RETURN
        0xD2: "OP_RETURN_210",
        0xD9: "OP_RETURN_217",
        0xDA: "OP_RETURN_218",
        0xF9: "OP_RETURN_249",
    }

    commands = []
    b = 0
    while b < len(byte_stream):
        byte = byte_stream[b]
        if byte < 0x02:
            commands.append(byte)
        elif byte >= 0x52 and byte <= 0x60:
            commands.append(byte - 0x50)
        elif byte >= 0x02 and byte <= 0x4B:
            commands.append(hexlify(byte_stream[b + 1 : b + 1 + byte]))
        elif byte >= 0xBA:
            commands.append(f"OP_RETURN_{byte-0xba+186}")
        else:
            if byte in opcodes:
                commands.append(opcodes[byte])
            else:
                commands.append(f"@@@@Invalid (0x{byte:02x})")
                # raise ValueError(f"Optcode '{byte}' is not known")
        b += 1
    return commands


def parse_varint(hex_stream: str) -> Tuple[int, int]:
    """
    Parse a varint from the hex stream.

    See https://learnmeabitcoin.com/technical/varint

    Parameters
    ----------
    hex_stream : str

    Returns
    -------
    (varint value, next_pos)
    """
    hex_chars_per_byte = 2
    if hex_stream.startswith("fd"):
        start = 2
        next_bytes = 2
    elif hex_stream.startswith("fe"):
        start = 2
        next_bytes = 4
    elif hex_stream.startswith("ff"):
        start = 2
        next_bytes = 8
    else:
        next_bytes = 1
        start = 0
    return (
        hex_to_num(hex_stream[start : next_bytes * hex_chars_per_byte]),
        start + next_bytes * hex_chars_per_byte,
    )


def disect_transaction(tx: str) -> Transaction:
    # 1 hex character can encode 16 values
    # 1 Byte has 8 Bit and thus 2**8 = 256 values
    # 2 hex characters can encode 16**2 = 256 values
    # Hence: 2 hex chars = 1 Byte
    hex_chars_per_byte = 2

    # Get the transaction protocol version number (typically "1")
    char_current = 0
    char_next = char_current + 4 * hex_chars_per_byte
    version_number = hex_to_num(tx[char_current:char_next])

    # What is this?
    char_current = char_next
    char_next = char_current + 1 * hex_chars_per_byte
    marker = tx[char_current:char_next]
    print(f"{marker=}")
    assert marker == "00"

    char_current = char_next
    char_next = char_current + 1 * hex_chars_per_byte
    flag = tx[char_current:char_next]
    print(f"{flag=}")
    assert flag == "01"

    # Get the input counter
    char_current = char_next
    input_counter, char_next_add = parse_varint(tx[char_current:])
    char_next = char_current + char_next_add

    tx_ins = []
    for _ in range(input_counter):
        # Get the transaction ID
        char_current = char_next
        char_next = char_current + 32 * hex_chars_per_byte
        tx_id = reorder(tx[char_current:char_next])

        # tx_index
        char_current = char_next
        char_next = char_current + 4 * hex_chars_per_byte
        tx_index = hex_to_num(tx[char_current:char_next])

        # Get the input script length
        char_current = char_next
        input_script_length, char_next_add = parse_varint(tx[char_current:])
        char_next = char_current + char_next_add

        # Get the input script
        char_current = char_next
        char_next = char_current + input_script_length * hex_chars_per_byte
        input_script = tx[char_current:char_next]

        # Sequence number: What is it used for?
        char_current = char_next
        char_next = char_current + 4 * hex_chars_per_byte
        sequence = hex_to_num(tx[char_current:char_next])
        tx_ins.append(
            TxIn(
                tx_id=tx_id,
                tx_index=tx_index,
                script=input_script,
                sequence=sequence,
            )
        )

    # Get the number of transaction outputs for further parsing
    char_current = char_next
    output_count, char_next_add = parse_varint(tx[char_current:])
    char_next = char_current + char_next_add

    # Parse the transaction outputs
    tx_outs = []
    for _out_index in range(output_count):
        # Number of Bitcoin
        char_current = char_next
        char_next = char_current + 8 * hex_chars_per_byte
        satoshi = hex_to_num(tx[char_current:char_next])

        # Get the script length for further processing
        char_current = char_next
        out_script_length, char_next_add = parse_varint(tx[char_current:])
        char_next = char_current + char_next_add

        # Get the output script
        char_current = char_next
        char_next = char_current + out_script_length * hex_chars_per_byte
        out_script = tx[char_current:char_next]

        print("-" * 80)
        print(bytes_to_asm(unhexlify(out_script)))

        tx_outs.append(TxOut(satoshi=satoshi, script=out_script))

    # Get witnesses
    stack_items = []
    for _ in range(input_counter):
        char_current = char_next
        nb_stack_items, char_next_add = parse_varint(tx[char_current:])
        char_next = char_current + char_next_add

        stack_items_sub = []
        for _ in range(nb_stack_items):
            char_current = char_next
            stack_item_length, char_next_add = parse_varint(tx[char_current:])
            char_next = char_current + char_next_add

            # Get the stack item
            char_current = char_next
            char_next = char_current + stack_item_length * hex_chars_per_byte
            stack_item = tx[char_current:char_next]

            stack_items_sub.append(stack_item)
        stack_items.append(stack_items_sub)
    witness = Witness(stack_items=stack_items)

    # Locktime is the earlies time a transaction can be used
    # https://medium.com/summa-technology/bitcoins-time-locks-27e0c362d7a1
    from datetime import datetime, timezone

    locktime = hex_to_num(tx[-4 * hex_chars_per_byte :])
    unix_datetime = datetime.fromtimestamp(locktime, timezone.utc)
    return Transaction(
        version_number=version_number,
        marker=marker,
        flag=flag,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        witness=witness,
        locktime=locktime,
    )


# https://blockchain.info/tx/30713d08afa548d3465e380d6e1837354b29a1b6707e2a913b27776cf305fda4?format=json
# tx = disect_transaction("010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff5403df550a1b4d696e656420627920416e74506f6f6c373138fd004702c13ba070fabe6d6d6d9986fd3aedb9f8b00fab3c74c2e1d399fd0e6bc1d964aa57a08f78ac2d648002000000000000001eb50000c1377c00ffffffff04653c3a2a000000001976a91411dbe48cc6b617f9c6adaf4d9ed5f625b1c7cb5988ac0000000000000000266a24aa21a9ede0721e21cc17367eb4fcccf94c7e6ebc54757a693515f809307d4d6a31e0c8500000000000000000266a24b9e11b6d6eab9aaf2ccdc3cb05fb15989c512b84c8ef5f498559cd4d66e6104de8f9cdb100000000000000002b6a2952534b424c4f434b3a93320d7a461a95b953bd18e40aa031b5470d6258ccd82011999a5b290031529c0120000000000000000000000000000000000000000000000000000000000000000000000000")

# https://blockchain.info/tx/5199467818921262400267588408f481ab30db455eef700bd965fab9bfa10dec?format=hex
# tx = disect_transaction("010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff64039d560a2cfabe6d6d0d5545b446f0e9c35bb42c6fec8c9a6c3ef4b6f64d9a01e2169f01dc5a77d50f10000000f09f909f082f4632506f6f6c2f104d696e656420627920626967686f726e00000000000000000000000000000000000000050022e600000000000004a4858c27000000001976a914c825a1ecf2a6830c4401620c3a16f1995057c2ab88ac0000000000000000266a24aa21a9ed8630f428a357cf72ae52cd6f78d3e1156a6496682e54fee6fc6bc8ccb8a1d6e900000000000000002c6a4c2952534b424c4f434b3a23a972ed54a376c793d6ccd71eb3952535b81e8c040392c426da052d003160ee0000000000000000266a24b9e11b6d03a83f229005077a5c750dc9f3944de70ba59c0ac9874d2eb97770c25e60a27001200000000000000000000000000000000000000000000000000000000000000000a8c91d3f")
# print(tx.json(indent=4))

# tx = disect_transaction("010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff64039d560a2cfabe6d6d0d5545b446f0e9c35bb42c6fec8c9a6c3ef4b6f64d9a01e2169f01dc5a77d50f10000000f09f909f082f4632506f6f6c2f104d696e656420627920626967686f726e00000000000000000000000000000000000000050022e600000000000004a4858c27000000001976a914c825a1ecf2a6830c4401620c3a16f1995057c2ab88ac0000000000000000266a24aa21a9ed8630f428a357cf72ae52cd6f78d3e1156a6496682e54fee6fc6bc8ccb8a1d6e900000000000000002c6a4c2952534b424c4f434b3a23a972ed54a376c793d6ccd71eb3952535b81e8c040392c426da052d003160ee0000000000000000266a24b9e11b6d03a83f229005077a5c750dc9f3944de70ba59c0ac9874d2eb97770c25e60a27001200000000000000000000000000000000000000000000000000000000000000000a8c91d3f")
# print(tx.json(indent=4))

# 0100
# 0000
# 0001
# 010000000000000000000000000000000000000000000000000000000000000000ffffffff64039d560a2cfabe6d6d0d5545b446f0e9c35bb42c6fec8c9a6c3ef4b6f64d9a01e2169f01dc5a77d50f10000000f09f909f082f4632506f6f6c2f104d696e656420627920626967686f726e00000000000000000000000000000000000000050022e600000000000004a4858c27000000001976a914c825a1ecf2a6830c4401620c3a16f1995057c2ab88ac0000000000000000266a24aa21a9ed8630f428a357cf72ae52cd6f78d3e1156a6496682e54fee6fc6bc8ccb8a1d6e900000000000000002c6a4c2952534b424c4f434b3a23a972ed54a376c793d6ccd71eb3952535b81e8c040392c426da052d003160ee0000000000000000266a24b9e11b6d03a83f229005077a5c750dc9f3944de70ba59c0ac9874d2eb97770c25e60a27001200000000000000000000000000000000000000000000000000000000000000000a8c91d3f

# https://blockchain.info/tx/1ac73c87b60b130845139ba3534a894ca6e072607a1f1cfec4aef36713f0cdbd?format=hex
tx = disect_transaction(
    "010000000001093bec230ae178663dbdeddf2570e9f193d85bae1ae8cd409f394d7a39642e3be30200000017160014c64e18131f87661e956c1d659538b9ed34462794ffffffff4b5729b4b2f7bfc29afffd846d2d9492972cfd4f58eceb3d4462a74d3d479f090400000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffff68be5a96fe56faeb5640d2857fae7cbc601e1bf22e614857e2b79956c9c6a23a0000000017160014c64e18131f87661e956c1d659538b9ed34462794fffffffffd0543dc331112236a66fee55daca9b6c65cfdbc4c2efb457b421a047f51db150800000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffff157a3017a1a701656354e9fe6745d1fec447af1a6bd66b5f07565c88128828480100000017160014c64e18131f87661e956c1d659538b9ed34462794ffffffff5eb085c2aacfd9595576205bfa3957eedd28b244e53c6986dedbef7c21abdd810500000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffffc9ce162d3571164219da63b640c795540004fe6600385c4732fe4de99efa5f1b0100000017160014b53f8c3d65ffbc8d6718db8d907857a8ed9d6b1bffffffff1f3dd62e981ac9b6e73a329c0ab531f1d1769ce6d7f8e6a63edea7069ca72a980200000017160014c64e18131f87661e956c1d659538b9ed34462794fffffffffe14856d28bfa22fc53ccf972b4918cabb3a2f6924f2c0fcf6e18080cf62fcbc0d00000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffff02a0d9ea040000000017a91415b14171dab0994bf9d2362201b8a8d92311706287cc9c0e000000000017a9144f3ec7767c9c4b9982baadd98f36c2bbe8da955c870247304402204bff71e5000356f0a512df30cce921254ded0f30060fb50f404aeb5c64300ef702202e676b9535584e22cb6a63b55ff8c95398c8f5a4f4b56507ab87f45ba8964fb001210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c024830450221008911f8dd80e65af75838b9e922844fe6b870b2d5297993beca928d983070b63f02203dbc99b5fdba221eb095f2c9280279a455e7ba68122d3ec192f9915071caf7cf01210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d902473044022027a6216c3335c26544bb705e60eadc211de533ecabf74d1869bb1a56dc20e4f7022024da9adc984ee5a3cece1d10efac1ce6ebf4ecfe94d21516ba68ef149d4caf1c01210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c02483045022100c12d3774609c5b68938832e56eee3bc035ce8d6b2af3b8e51ddb1e30416742df02205569deef3c6eff8190c705af3b29381a5e07d6b008a853bcb653f2bcae154b8801210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d90247304402204d7036a3bd8c7b8f571834be38b849c44059500aa7f0de5cf7bc8f8732001e4002203c51743865e9c25dea3ecdff24bfd6ee15bf6a6a2bafdd669bee6aa3998a2cbf01210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c02483045022100b4b4289409de1ea1b77a843a23d1621894cde5560402e86f59702f190cf4070c02200f64471000a50af384b2e2e71faea529d30e8103c64be0daef4c64aeee6d752b01210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d902483045022100d98712b6dc33b118d80a3a50421dd89d0ad4b2dc4d8122f15b3bcfbeab5f098b02205d4634091f517cc6616c16f1521ba199d78e9288963a199d8f24bee6cd61f07b012102cd923d82b5a698c594b0545dce0628f62be4caa4316f1b384bc91d9ebeedd35a02483045022100a8d2646d76d50ef12e2fba11b708ed2005f228c31457b2de7b77d10f1ab34f4d02204dad17ff08990f444c76d41121732c0a6b553626abab23ef420cf1bcb4f91c2a01210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c02473044022025e6318e264ff9507134f6c80fe1741822d7275f83a363eae0e5b360fa78eb5902203df5c4b636446409f846d95398beed9cdf5304a0f3157d90637578576064e20601210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d900000000"
)
print(tx.json(indent=4))
