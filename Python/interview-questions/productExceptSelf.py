from functools import reduce
from operator import __mul__


def productExceptSelf(nums, m):
    n = len(nums)
    p_forward = [1]
    for el in nums:
        p_forward.append(p_forward[-1] * el) % m
    p_forward = p_forward

    p_backward = [1]
    for el in nums[::-1]:
        p_backward.append(p_backward[-1] * el)
    p_backward = p_backward[::-1][1:] % m
    s = 0
    for i in range(n):
        s += p_forward[i] * p_backward[i]
        s %= m
    return s % m


#######################
def productExceptSelf(nums, m):
    p = 1
    s = 0
    for num in nums:
        s = (s * num + p) % m
        p = (p * num) % m
    return s


if __name__ == "__main__":
    import doctest

    doctest.testmod()
