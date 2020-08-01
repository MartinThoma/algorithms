# Core Library modules
import datetime
from unittest import mock

# First party modules
from mock_example import generate_filename


class NewDate(datetime.datetime):
    @classmethod
    def now(cls):
        return cls(1990, 4, 28)


def test_generate_filename():
    datetime.datetime = NewDate
    assert generate_filename() == "1990-04-28.png"
