import os
import sys
import time

version = sys.version_info
version = f"{version.major}.{version.minor}.{version.micro}"


if os.path.isfile("numbers-tmp.txt"):
    os.remove("numers-tmp.txt")

t0 = time.time()
with open("numbers-large.txt") as fin, open("numers-tmp.txt", "w") as fout:
    for line in fin:
        fout.write(line)
t1 = time.time()


print("Python {}: {:0.0f}s".format(version, t1 - t0))
