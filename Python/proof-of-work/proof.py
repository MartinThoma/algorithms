import hashlib
import itertools
import random
import time
from typing import Tuple


def find_hash(start: str = "00") -> Tuple[str, int]:
    nb_probed = 0
    for probe in generate_random_str():
        nb_probed += 1
        hashval = hashlib.sha512(bytes(probe, "utf8"))
        if hashval.hexdigest().startswith(start):
            return probe, nb_probed


def generate_random_str(length: int = 4) -> str:
    abc = "abcdefghijklmnopqrstuvwxyz"
    chars = list(abc + abc.upper() + "0123456789" + ' !"§$%&/()=?+-')
    while True:
        print(f"Length={length}")
        for string in itertools.product(chars, repeat=length):
            random_str = "".join(string)
            yield random_str
        length += 1


t0 = time.time()
probe, nb_probed = find_hash("0" * 6)
t1 = time.time()
hashval = hashlib.sha512(bytes(probe, "utf8")).hexdigest()
print(f"{probe=}; {hashval=}; nb_probed={nb_probed:,}")
