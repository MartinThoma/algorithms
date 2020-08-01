import datetime


def generate_filename():
    return f"{datetime.datetime.now():%Y-%m-%d}.png"
