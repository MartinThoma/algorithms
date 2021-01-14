import hashlib
import time
import zlib
from typing import List


def get_word_list(filepath: str = "words.txt") -> List[str]:
    with open(filepath) as fp:
        return [line.strip() for line in fp]


def test_hash_functions(hash_functions):
    t0 = time.time()
    words = get_word_list()
    t1 = time.time()
    print(f"Time loading the words: {t1 - t0:0.1f}s")
    name = "Hash function"
    collisions_str = "collisions"
    header = f"{name:<20} {collisions_str:<15} ns/value"
    print(header)
    print("-" * len(header))
    for hash_function, name in hash_functions:
        hash2word = {}
        collisions = []
        t0 = time.time()
        for word in words:
            hash_value = hash_function(word)
            if hash_value not in hash2word:
                hash2word[hash_value] = word
            else:
                collisions.append((hash2word[hash_value], word))
        t1 = time.time()
        print(
            f"{name:<20} {len(collisions):<15,} {(t1-t0)*10**9/len(words):7.1f} ns/value"
        )
        for collision in collisions[:10]:
            print(f"\t{collision}")


def str_md5(string):
    return hashlib.md5(string.encode()).hexdigest()


def str_sha1(string):
    return hashlib.sha1(string.encode()).hexdigest()


def str_sha256(string):
    return hashlib.sha256(string.encode()).hexdigest()


def str_crc32(string):
    return hex(zlib.crc32(string.encode()) & 0xFFFFFFFF)


def str_adler32(string):
    return zlib.adler32(string.encode())

def str_xor(string):
    curr = 0
    for char in string:
        curr ^= ord(char)
    return curr


if __name__ == "__main__":
    test_hash_functions(
        [
            (str_md5, "md5"),
            (str_sha1, "sha1"),
            (str_sha256, "sha256"),
            (str_crc32, "crc32"),
            (str_adler32, "adler32"),
            (str_xor, "char_xor")
        ]
    )
