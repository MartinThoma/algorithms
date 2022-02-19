import typer
from pathlib import Path
from typing import List
import math

app = typer.Typer()

@app.command()
def encode(to_encode: Path, wordlist: Path):
    words = read_words(wordlist)
    assert len(words) >= 2, "We need at least two states to encode"

    # For simplicity, make sure we have a power of two
    basis = highest_power_of_2(len(words))
    bit_per_word = math.log(basis, 2)
    print(
        f"Use basis {basis} for {len(words)}. This means every word can "
        f"encode {bit_per_word}-bit chunks.")
    words = words[:basis]

    with open(to_encode, "rb") as fp:
        data = fp.read()

    chunks = math.ceil(len(data) * 8 / bit_per_word)
    print(f"Read {len(data)} bytes. This means we need {chunks:,} chunks.")
    print(data[0])
    #for i in range(0, len(data), bit_per_word):



def highest_power_of_2(n: int) -> int:
    p = int(math.ceil(math.log(n, 2)))
    while not (n < 2**(p+1)):
        p += 1
    while not (2**p <= n):
        p -= 1
    assert 2**p <= n < 2**(p+1)
    answer = int(pow(2, p))
    return answer


def read_words(wordlist: Path) -> List[str]:
    with open(wordlist) as fp:
        data = fp.read()
    return data.split("\n")


@app.command()
def decode():
    ...

if __name__ == "__main__":
    app()
