import json
import sys
import time

import pandas as pd
from pympler import asizeof


class LogMsgSlots:
    __slots__ = "level", "message", "timestamp"

    def __init__(self, level, message, timestamp):
        self.level = level
        self.message = message
        self.timestamp = timestamp


class LogMsg:
    def __init__(self, level, message, timestamp):
        self.level = level
        self.message = message
        self.timestamp = timestamp


def read_dicts(filepath):
    msgs = []
    with open(filepath) as fp:
        for line in fp:
            msgs.append(json.loads(line))
    return msgs


def read_objects(filepath):
    msgs = []
    with open(filepath) as fp:
        for line in fp:
            msg = json.loads(line)
            msgs.append(
                LogMsg(
                    level=msg["level"],
                    message=msg["message"],
                    timestamp=msg["timestamp"],
                )
            )
    return msgs


def read_slots(filepath):
    msgs = []
    with open(filepath) as fp:
        for line in fp:
            msg = json.loads(line)
            msgs.append(
                LogMsgSlots(
                    level=msg["level"],
                    message=msg["message"],
                    timestamp=msg["timestamp"],
                )
            )
    return msgs


def read_pd(filepath):
    df = pd.read_json(filepath, lines=True)
    return df


if __name__ == "__main__":
    filepath = "structured.log"
    methods = [
        ("Python Dicts", read_dicts),
        ("Python Objects", read_objects),
        ("Pandas", read_pd),
        ("Slots", read_slots),
    ]
    baseline_size = None
    baseline_speed = None
    for method_name, function in methods:
        t0 = time.time()
        content = function(filepath)
        t1 = time.time()
        size = asizeof.asizeof(content)
        speed = t1 - t0
        if baseline_size is None:
            baseline_size = size
            baseline_speed = speed
        print(
            f"{method_name:>15}: "
            f"{size:>20,} Byte ({size/baseline_size*100:0.0f}%), "
            f"{speed:0.2f}s ({speed/baseline_speed*100:0.0f}%)"
        )
