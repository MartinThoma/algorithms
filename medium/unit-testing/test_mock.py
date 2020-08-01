from mock_example import generate_filename
from unittest import mock
import datetime


def test_generate_filename():
    with mock.patch(
        "mock_example.datetime.datetime.now", return_value=datetime.datetime(2014, 6, 2)
    ):
        assert generate_filename() == "2014-06-02.png"
