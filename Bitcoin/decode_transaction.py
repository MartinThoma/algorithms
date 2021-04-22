from pydantic import BaseModel  # pip install pydantic
from typing import List, Tuple, Optional
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
    marker: Optional[str]
    flag: Optional[str]
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

    # Marker
    reset_char_current = char_current
    reset_char_next = char_next
    char_current = char_next
    char_next = char_current + 1 * hex_chars_per_byte
    marker = tx[char_current:char_next]
    print(f"{marker=}")
    # assert marker == "00"
    if marker != "00":
        # This is an early transaction without a marker
        marker = None
        char_current = reset_char_current
        char_next = reset_char_next

    # Flag
    if marker is None:
        flag = None
    else:
        reset_char_current = char_current
        reset_char_next = char_next
        char_current = char_next
        char_next = char_current + 1 * hex_chars_per_byte
        flag = tx[char_current:char_next]
        print(f"{flag=}")
        # assert flag == "01"
        if flag != "01":
            # This is an early transaction without a flag
            flag = None
            char_current = reset_char_current
            char_next = reset_char_next

    # Get the input counter
    char_current = char_next
    input_counter, char_next_add = parse_varint(tx[char_current:])
    char_next = char_current + char_next_add

    tx_ins = []
    for _input_i in range(input_counter):
        # Get the transaction ID
        char_current = char_next
        char_next = char_current + 32 * hex_chars_per_byte
        tx_id = reorder(tx[char_current:char_next])

        # tx_index
        char_current = char_next
        char_next = char_current + 4 * hex_chars_per_byte
        tx_index = hex_to_num(tx[char_current:char_next])

        # Get the unlocking script length
        char_current = char_next
        unlocking_script_length, char_next_add = parse_varint(tx[char_current:])
        char_next = char_current + char_next_add

        # Get the input script
        char_current = char_next
        char_next = char_current + unlocking_script_length * hex_chars_per_byte
        unlocking_script = tx[char_current:char_next]
        print(f"{_input_i=}")
        print(unhexlify(unlocking_script))

        # Sequence number: What is it used for?
        char_current = char_next
        char_next = char_current + 4 * hex_chars_per_byte
        sequence = hex_to_num(tx[char_current:char_next])
        tx_ins.append(
            TxIn(
                tx_id=tx_id,
                tx_index=tx_index,
                script=unlocking_script,
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

        # Get the locking script length for further processing
        char_current = char_next
        out_script_length, char_next_add = parse_varint(tx[char_current:])
        char_next = char_current + char_next_add

        # Get the locking script
        char_current = char_next
        char_next = char_current + out_script_length * hex_chars_per_byte
        locking_script = tx[char_current:char_next]
        print(f"{_out_index=}")
        print(unhexlify(locking_script))

        print("-" * 80)
        print(bytes_to_asm(unhexlify(locking_script)))

        tx_outs.append(TxOut(satoshi=satoshi, script=locking_script))

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


#https://blockchain.info/tx/30713d08afa548d3465e380d6e1837354b29a1b6707e2a913b27776cf305fda4?format=json
tx = disect_transaction("0100000001bb81d5bbba37eed68e1d97d4af1dc799c72f156b520e413073363e44c745f6000a0000008b483045022100b7393ff959120e3ccb5284e3cf2eaa200235643a1549a4e6faaa911619089e2b02207b677827c7beeb53503e016a8dd29164d07cb79f0f1e058df9b8dfa3568d0290014104c4b7a7f7bb2c899f4aeab75b41567c040ae79506d43ee72f650c95b6319e47402f0ba88d1c5a294d075885442679dc24882ea37c31e0dbc82cfd51ed185d7e94ffffffff0b2b4200000000000017a914c29b367fe07d6eb8c8c4169c9ccebd1b29ef47a6870f571000000000001976a9141ff86c091106944ab141e69868b2016b6fab1bf388ac312304000000000017a91477fdd156a45076e5e40e1eaac82e2a365029c64a87e52f8d000000000017a9140d29c2a4f749c2789760f9c7c564f54bfb88222887f6d213000000000017a914f0339060b2b2b49fd9528a3fa63f91c579b44fa78762295b00000000001976a91405a17c67075c932d581a94af7387d3ae393c2a2788acfc9e04000000000017a91474329305901e3bfd8fe02eb525e638954d4c8d0587085ade01000000001976a9140183eade07a9bfd9ab764a73fe6bf1b005238b7288ac83b40900000000001976a914bf326d0ac492d5eb8bd5a9983e332c171fd4872388ac18b40200000000001976a914229d91d59e3a0fce29ed4cb43ad924cdf9865d3788ac9769f105000000001976a9147ddb236e7877d5040e2a59e4be544c65934e573a88ac00000000")

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
# tx = disect_transaction("010000000001093bec230ae178663dbdeddf2570e9f193d85bae1ae8cd409f394d7a39642e3be30200000017160014c64e18131f87661e956c1d659538b9ed34462794ffffffff4b5729b4b2f7bfc29afffd846d2d9492972cfd4f58eceb3d4462a74d3d479f090400000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffff68be5a96fe56faeb5640d2857fae7cbc601e1bf22e614857e2b79956c9c6a23a0000000017160014c64e18131f87661e956c1d659538b9ed34462794fffffffffd0543dc331112236a66fee55daca9b6c65cfdbc4c2efb457b421a047f51db150800000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffff157a3017a1a701656354e9fe6745d1fec447af1a6bd66b5f07565c88128828480100000017160014c64e18131f87661e956c1d659538b9ed34462794ffffffff5eb085c2aacfd9595576205bfa3957eedd28b244e53c6986dedbef7c21abdd810500000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffffc9ce162d3571164219da63b640c795540004fe6600385c4732fe4de99efa5f1b0100000017160014b53f8c3d65ffbc8d6718db8d907857a8ed9d6b1bffffffff1f3dd62e981ac9b6e73a329c0ab531f1d1769ce6d7f8e6a63edea7069ca72a980200000017160014c64e18131f87661e956c1d659538b9ed34462794fffffffffe14856d28bfa22fc53ccf972b4918cabb3a2f6924f2c0fcf6e18080cf62fcbc0d00000017160014b3fc79351bbe69fffa8281bf7cddb0bf7245670effffffff02a0d9ea040000000017a91415b14171dab0994bf9d2362201b8a8d92311706287cc9c0e000000000017a9144f3ec7767c9c4b9982baadd98f36c2bbe8da955c870247304402204bff71e5000356f0a512df30cce921254ded0f30060fb50f404aeb5c64300ef702202e676b9535584e22cb6a63b55ff8c95398c8f5a4f4b56507ab87f45ba8964fb001210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c024830450221008911f8dd80e65af75838b9e922844fe6b870b2d5297993beca928d983070b63f02203dbc99b5fdba221eb095f2c9280279a455e7ba68122d3ec192f9915071caf7cf01210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d902473044022027a6216c3335c26544bb705e60eadc211de533ecabf74d1869bb1a56dc20e4f7022024da9adc984ee5a3cece1d10efac1ce6ebf4ecfe94d21516ba68ef149d4caf1c01210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c02483045022100c12d3774609c5b68938832e56eee3bc035ce8d6b2af3b8e51ddb1e30416742df02205569deef3c6eff8190c705af3b29381a5e07d6b008a853bcb653f2bcae154b8801210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d90247304402204d7036a3bd8c7b8f571834be38b849c44059500aa7f0de5cf7bc8f8732001e4002203c51743865e9c25dea3ecdff24bfd6ee15bf6a6a2bafdd669bee6aa3998a2cbf01210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c02483045022100b4b4289409de1ea1b77a843a23d1621894cde5560402e86f59702f190cf4070c02200f64471000a50af384b2e2e71faea529d30e8103c64be0daef4c64aeee6d752b01210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d902483045022100d98712b6dc33b118d80a3a50421dd89d0ad4b2dc4d8122f15b3bcfbeab5f098b02205d4634091f517cc6616c16f1521ba199d78e9288963a199d8f24bee6cd61f07b012102cd923d82b5a698c594b0545dce0628f62be4caa4316f1b384bc91d9ebeedd35a02483045022100a8d2646d76d50ef12e2fba11b708ed2005f228c31457b2de7b77d10f1ab34f4d02204dad17ff08990f444c76d41121732c0a6b553626abab23ef420cf1bcb4f91c2a01210349a73ba7663278244b0d7d40c839d13f945c185c6a78bf2c08e02daa8fea054c02473044022025e6318e264ff9507134f6c80fe1741822d7275f83a363eae0e5b360fa78eb5902203df5c4b636446409f846d95398beed9cdf5304a0f3157d90637578576064e20601210236e81fbc1bcd58fd428c91b524062fb8df3e4a342921371cb4a1b76c29a973d900000000")
# print(tx.json(indent=4))

#tx = disect_transaction("01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000")
#print(tx.json(indent=4))

# https://blockchain.info/tx/d8459c53ff634dbf15168d44c6c8eff8656eebd12244f5cf8fea779c00041cdc?format=hex
#tx = disect_transaction("010000000f486d93aab1585af81d73f118a23c8b94c96507992889e2c84a90d3eed92b8ec5000000008b4830450221009d9a8121e57d7d1a2704ddb26967cdd2d65c8654f0e6d4a03bb36ff2f203ea68022013667854b5417bee46671482f626789c90c73cfeb5501f57f87415de7bbe31c0014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff4e9b62c9440f56e5b2bfe72429884eb1fcab30a34b35a327c791d4af3f7be5a8000000008a47304402200e47f3a0308bd532275a4753fa5810c84c12b1aa87c79a4f905123dbac81128a022047d444029fc4321f82a23c5fd8139ea04106618c3861a726101fcdaecd238cbe014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff5610374bd49c5c29bf6405f44b894d60fc6b0477a6d990f75fee69d97231f0ef050000008b483045022100c26069540463547436518e73f3f23e5d1c9ec94b8f5df2bb1727151418e97d43022030037e8bd878c12f093857af62f30a9160d07e3b051cdd9a880fcdd04336e0ee014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffffe41a4df4eb83d1cbce1924b0eab3d42ce655f3e941870a361e20b7ba666948db000000008b483045022100af48d7eb2b5b5fe31c20c711550b41824ae0e42683a4b6c94e4b2489f13fe2dd0220076cb428003fca03f6677c3e95d8b718b1fbbb9646451fafdbd0be2633a93689014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffffe5e0710d19964c38fb04f6a41e70c782ca1b3e8deeb1a3ebaf5b4f9768052d20010000008a473044022003bcd7f5db7f89578ec059be2b3dc1fd7a01940e5b5621f0cb68db152cde11c9022016df1393306a339b730d782a64578f67fc8a7daa61f5d443adaa3fc6851ddaee014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafefffffff0f893786383c9bfbf9466f600d638ca1754f3703a47b9357b2f2ec79cfa4e60000000008a473044022055cc13094af20d9582d0dc9cdf56a649def65870f85e3eaab80b467449b23a36022042e27695b73c984c928ff47e1020b864a0e29d338171412d2b237597bfcdeb42014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafefffffffad1063f1f7b052d0c2b62595109ab32f6cf9fa9493539ca5993f1e55f4e9ebb010000008b483045022100f8c684dd955490870b42ec11428c5fadc53167231a1a3126716b552f7eee595302200adceecaf132f0ec81ee901ee16a83be86cd0212a1fc38f71e33d1f312470584014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff193a3cd7e9a79ac1549aeec7585416bfe707537fe699caa9ef73f2d30f157fa1010000008a4730440220335fefa295f123caf2abb5f0994944aaccccef827b1d9536bf8d7608961b2ca702207ccf5260b63a749d5b53f5f996a211aab6e467c77f95f5be9a9461d4a4b7bb83014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff123c9ed8564fe3a837ec3f851ed005f8d4edd25132af90c7586a93d3642016a60c0000008a4730440220295810d84987f74e3807accad6acc9ce5ed8aa9e8f6695a2279392a5f75403e3022075c6365da1483b676e823258eda2cc783c7a59b254cd7c784c1ceee6a4648618014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff968e16f508ca17e7df73fed2b8c250bf43e3ed1c3fea713e2128b3c3d3bdf0d8000000008b483045022100b386c7dce1f2b5a9086309baf5bf944654299852e919b7f74624553892a774f602201bfae2ff1d3d5ce06511426c5d7357ed1b6f683ebeb93d5aa96b11c47f36bb22014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff26653dbcaab1f2469611cb8af8a7ac559c913adc164ab3e564ae371c6e57794d000000008a47304402206fceebf96419a694ddbc2753fecb021889d54a7c1b0c3aa70d1d39ed52345e14022043e7f2ad634c0424f58ce8e79bc41b97809a8bcd818e0651c11c5c0886a0e527014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff6e89742bdd4f1cb00dd16adfb63c6788eecff03d6bade7f1d4d94ad8fac8b2d4000000008b483045022100bd72bc3d0161b2de21537c68c2cf1747be443d6971d83a289b7e305bdc451b3102202277ce9f16a497697eef266f946579905d0ab5d778e1e892c6e859159ca33480014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff776ad057f7f4edf007dca8de551609b8c1897de6f20330ecd83a8b992ae64939010000008a473044022043f1c96ae6c980b503f8452a6f74dfe615b72548bf90ef525fb0e6425a2beae902205a2d1130457ad6e72f486de6de47b5d4f282755276249c46334995bc130e4fc9014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff816489f8bb0453c0049fd39ffa083b7822f98f9ac03921274987bbf736c1501e000000008a47304402204922439e9507cc06e3f138eeeb2ccdaf40cea724f020f233a6d83317071dad14022036637b0be19fede50bf86f6d2bc6b311468de3e94ddebe5fea6b78ae50dbafb6014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff8cca953681f0dc444be57f7cf534af89574e458c7f491a6cd6a6392509053773000000008a473044022057d798f67c45d65520e726c7e76701df19d933be747449cac02b45d6573d1db60220387bb79c5f618df8a27da0a62b7d67ec4d3c5cb52921637a76fe40dd1e094c44014104778f93e3cf4db394e21947771e0bceb5950440432bff63b50b35dd0f7303b243cade6bea4b92972018140786c4585d8b345361b90b4c1db01d2e9cef01048fdafeffffff0180f0fa02000000001976a9146549d32432babee71958ba7477f1250533ce7cec88ac2a4a0600")

# https://blockchain.info/tx/057954bb28527ff9c7701c6fd2b7f770163718ded09745da56cc95e7606afe99?format=hex
#tx = disect_transaction("01000000000101ff133ad017deef919cb97f2d092884ad60cf0c24926d6500d2f581cb36b162540400000000feffffff03e4970600000000001976a914ad47d7e9b5b68c6598446d0b376f57eb5ba49f5588ace4970600000000001976a914758ef88abc7dccfb1d4f3e81b561a9776d9b9b1b88ac0000000000000000486a46446f206e6f74206265206f766572636f6d65206279206576696c2c20627574206f766572636f6d65206576696c207769746820676f6f64202d20526f6d616e732031323a323102483045022100ec782550ed5fd965c9859746d34dfa1f5375eea867188e6599b55fa1e03d38a802205a81c5320f6bfe288fd90c69021174e3e645299b73a54a18ae7210ec8349e262012103070e0d1380e355f13ce8f58283c1bdd53d2bfd667db1982ca2c8c51578596d6e00000000")


print(tx.json(indent=4))
