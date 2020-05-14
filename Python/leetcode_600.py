from typing import Dict
from math import floor, log

from functools import lru_cache

d = {
    # generate_d
    0: 1,
    1: 2,
    2: 3,
    4: 4,
    8: 6,
    16: 9,
    32: 14,
    64: 22,
    128: 35,
    256: 56,
    512: 90,
    1024: 145,
    2048: 234,
    4096: 378,
    8192: 611,
    16384: 988,
    32768: 1598,
    65536: 2585,
    131072: 4182,
    262144: 6766,
    524288: 10947,
    1048576: 17712,
    2097152: 28658,
    4194304: 46369,
    8388608: 75026,
    16777216: 121394,
    33554432: 196419,
    67108864: 317812,
    134217728: 514230,
    268435456: 832041,
    536870912: 1346270,
    # generate_d101x
    2: 3,
    5: 5,
    11: 8,
    23: 13,
    47: 21,
    95: 34,
    191: 55,
    383: 89,
    767: 144,
    1535: 233,
    3071: 377,
    6143: 610,
    12287: 987,
    24575: 1597,
    49151: 2584,
    98303: 4181,
    196607: 6765,
    393215: 10946,
    786431: 17711,
    1572863: 28657,
    3145727: 46368,
    6291455: 75025,
    12582911: 121393,
    25165823: 196418,
    50331647: 317811,
    100663295: 514229,
    201326591: 832040,
    402653183: 1346269,
}

b = {}


@lru_cache(maxsize=512)
def findIntegers(num: int) -> int:
    if num <= 9:
        return d[num]
    else:
        i = 7
        power = 3
        val = d[7]
        while i < num:
            val += d[2 ** (power - 1)]
            power += 1
            i = 2 ** power
        return brute_force(num)


def brute_force(num: int, start=0) -> int:
    sol = 0
    for i in range(start, num + 1):
        if "11" not in f"{i:b}":
            sol += 1
    return sol


def closest_power_of_two(x):
    return int(floor(log(x) / log(2)))


def brute_force_with_d(num: int, d: Dict[int, int]) -> int:
    if f"{num:b}".startswith("11"):
        # Before: 1458.925 vs 342.385
        # After: 1213.933 vs 251.989
        num_arr: List[int] = [1] * len(f"{num:b}")
        num_arr[1] = 0
        num = sum(d * 2 ** i for i, d in enumerate(num_arr[::-1]))

    start = 2 ** closest_power_of_two(num)
    sol = d[start]
    sol += brute_force(num, start=start + 1)
    return sol


def try3(num: int, d: Dict[int, int]) -> int:
    if f"{num:b}".startswith("11"):
        # Comparing with brute_force_with_d
        # 245.319 vs 162.209
        num_arr: List[int] = [1] * len(f"{num:b}")
        num_arr[1] = 0
        num = sum(digit * 2 ** i for i, digit in enumerate(num_arr[::-1]))
    if num in d:  # 10_111...111 or 2**i
        return d[num]
    # At this point, we have a 1011...111 number, but the 1-block at the end
    # has at leas one zero in it

    start = 2 ** closest_power_of_two(num)
    sol = d[start]
    sol += brute_force(num, start=start + 1)
    return sol


def try4(num: int, d: Dict[int, int]) -> int:
    if f"{num:b}".startswith("11"):
        # Comparing with try3
        # 162.209 vs
        num_arr: List[int] = [1] * len(f"{num:b}")
        num_arr[1] = 0
        num = sum(d * 2 ** i for i, d in enumerate(num_arr[::-1]))
    if num in d:  # 10_111...111 or 2**i
        return d[num]
    # At this point, we have a 1011...111 number, but the 1-block at the end
    # has at leas one zero in it
    #
    # We know the value for 1000...000, but we need the missing values from there
    #                   to  1011...111
    # This is the same as 0 to 11.111
    start = 2 ** closest_power_of_two(num)
    num_arr: List[int] = [int(digit) for digit in f"{num:b}"]
    num_arr[0] = 0
    assert num_arr[1] == 0, "was not 0 at pos 1!"
    num = sum(digit * 2 ** i for i, digit in enumerate(num_arr[::-1]))
    return d[start] - 1 + try4(num, d)


def generate_d():
    for i in range(30):
        num = 2 ** i
        val = brute_force(num)
        print(f"{num}: {val},")


def generate_d101x():
    for i in range(2, 30):
        num_arr: List[int] = [1] * i
        num_arr[1] = 0
        num = sum(digit * 2 ** i for i, digit in enumerate(num_arr[::-1]))
        val = brute_force_with_d(num, d)
        print(f"{num}: {val},")


def check(randvals=100):
    import time
    import random

    random.seed(0)
    brute_time = 0
    impr_time = 0
    for i in range(randvals):
        num = random.randint(0, 10 ** 8 + 1)
        print(f"num={num:,}, next2={2**closest_power_of_two(num):,}")
        t0 = time.time()
        v1 = try3(num, d)
        t1 = time.time()
        v2 = try4(num, d)
        t2 = time.time()
        brute_time += t1 - t0
        impr_time += t2 - t1
        assert v1 == v2, f"for {num:,}: {v1:,} vs {v2:,}"
        print(f"{t1- t0:0.3f}s vs {t2-t1:0.3f}s")
    print(f"{brute_time:0.3f} vs {impr_time:0.3f}")


check()


## Hard:
# * 97_956_359
# * 96_597_127
# * 85_956_173
# * 48_056_573
# * 82_996_081
