from functools import lru_cache


def houseRobber(nums):
    """
    >>> houseRobber([1, 3, 1, 3, 100])
    103

    >>> houseRobber([2, 1, 2, 6, 1, 8, 10, 10])
    26
    """
    return cached_robber(tuple(nums))


@lru_cache
def cached_robber(nums):
    if len(nums) == 0:
        return 0
    elif len(nums) <= 2:
        return max(nums)
    elif len(nums) == 3:
        return max(nums[0] + nums[2], nums[1])
    return max(cached_robber(nums[:-1]), cached_robber(nums[:-2]) + nums[-1])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
