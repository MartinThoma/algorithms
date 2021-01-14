import json
import random
from datetime import datetime, timedelta, timezone

import numpy as np


def main(nb_messages=1_000_000, max_length=50):
    current = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    with open("structured.log", "w") as fp:
        for i in range(nb_messages):
            current += timedelta(seconds=random.randint(1, 30))
            level = random.choice(["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"])
            length = random.randint(10, max_length)
            message = "".join(np.random.choice(list(chars), length))
            fp.write(
                json.dumps(
                    {
                        "level": level,
                        "message": message,
                        "timestamp": current.isoformat(),
                    }
                )
                + "\n"
            )


if __name__ == "__main__":
    main()
