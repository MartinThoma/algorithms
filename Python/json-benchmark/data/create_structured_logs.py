import json
import random
import string
from datetime import datetime

import numpy as np

random.seed(0)
np.random.seed(0)


def get_random_string(length):
    letters = "ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890"
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def create_random_datetime(from_date, to_date, rand_type="uniform"):
    """
    Create random date within timeframe.

    Parameters
    ----------
    from_date : datetime object
    to_date : datetime object
    rand_type : {'uniform'}

    Examples
    --------
    >>> random.seed(28041990)
    >>> create_random_datetime(datetime(1990, 4, 28), datetime(2000, 12, 31))
    datetime.datetime(1998, 12, 13, 23, 38, 0, 121628)
    >>> create_random_datetime(datetime(1990, 4, 28), datetime(2000, 12, 31))
    datetime.datetime(2000, 3, 19, 19, 24, 31, 193940)
    """
    delta = to_date - from_date
    if rand_type == "uniform":
        rand = random.random()
    else:
        raise NotImplementedError(f"Unknown random mode '{rand_type}'")
    return from_date + rand * delta


with open("structured-log.json", "w") as fp:
    for i in range(100_000):
        msg_length = random.randint(10, 500)
        data = {
            "timestamp": create_random_datetime(
                datetime(1970, 1, 1), datetime(2020, 9, 30)
            ).isoformat(),
            "level": random.choice(["INFO", "WARNING"]),
            "message": get_random_string(msg_length),
        }
        fp.write(json.dumps(data) + "\n")
