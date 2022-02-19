alphabet = "".join(chr(ord("a") + i) for i in range(26)) + " "


def derive_key(sentence: str) -> str:
    key = ""
    sentence = sentence.lower()
    for letter in sentence + "".join(alphabet):
        if letter not in key:
            key += letter
    return key


def encrypt(plain_text: str, key: str) -> str:
    mapping = {
        plain_char: cipher_char for plain_char, cipher_char in zip(key, alphabet)
    }
    return "".join(mapping[plain_char] for plain_char in plain_text)


def decrypt(cipher_text: str, key: str) -> str:
    mapping = {
        cipher_char: plain_char for plain_char, cipher_char in zip(key, alphabet)
    }
    return "".join(mapping[cipher_char] for cipher_char in cipher_text)


if __name__ == "__main__":
    sentence = "The quick brown fox jumps"
    key = derive_key(sentence)
    print(f"key: {key}")

    plain_text = "secret"
    cipher_text = encrypt(plain_text, key)
    print(f"cipher_text: {cipher_text}")

    recovered_plain = decrypt(cipher_text, key)
    print(f"recovered_plain: {recovered_plain}")
