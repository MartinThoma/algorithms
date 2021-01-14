import datetime
import logging
import sys

logger = logging.getLogger(__name__)


class OnWeekendOnlyErrorsFilter(logging.Filter):
    def filter(self, record):
        is_weekday = datetime.datetime.today().weekday() < 5
        return is_weekday or record.levelno >= logging.ERROR


# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.WARNING)
# stdout_handler.addFilter(OnWeekendOnlyErrorsFilter())
# logger.addHandler(stdout_handler)

# stderr_handler = logging.StreamHandler(sys.stderr)
# stderr_handler.setLevel(logging.WARNING)
# logger.addHandler(stderr_handler)

foo = None
logger.warning("Huh %s", foo)

try:
    1/0
except Exception as ex:
    logger.error("Error setting Ubuntu-R.ttf QFont: %s", ex)
