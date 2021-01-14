import json
import logging
import os
import sys
from typing import Optional

from pythonjsonlogger import jsonlogger


def is_local(local_str: Optional[str]) -> bool:
    if local_str is None or local_str.lower() in ["n", "0", "false", "no"]:
        return False
    else:
        return True


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)

if is_local(os.environ.get("LOCAL")):
    # https://docs.python.org/2/library/logging.html#logrecord-attributes
    formatter = logging.Formatter(
        "{asctime} [{levelname:<9}] {message}", "%H:%M:%S", style="{"
    )
    handler.setFormatter(formatter)
else:
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)

if __name__ == "__main__":
    logger.info("This is an info message")
    logger.error("This is an error message", extra={"ip": "10.12.13"})
