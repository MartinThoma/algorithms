import json
import logging
import os
import sys
from typing import Optional

import structlog


def is_local(local_str: Optional[str]) -> bool:
    if local_str is None or local_str.lower() in ["n", "0", "false", "no"]:
        return False
    else:
        return True


if is_local(os.environ.get("LOCAL")):
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # structlog.stdlib.render_to_log_kwargs,
            # structlog.processors.JSONRenderer(indent=None, sort_keys=True),
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
else:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # structlog.stdlib.render_to_log_kwargs,
            structlog.processors.JSONRenderer(indent=None, sort_keys=True),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


# logging.getLogger(__name__).setLevel(logging.INFO)
logger = structlog.getLogger(__name__)

if __name__ == "__main__":
    logger.info("This is an info message")
    logger.error("This is an error message", ip="10.12.13")
