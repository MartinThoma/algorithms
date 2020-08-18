import os
import shutil
import sys
import time


def main(big_filepath):
    target_dir = "radixsort_tmp"
    shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    prefix2file = {}
    for prefix in range(10, 100):
        chunk = os.path.abspath(f"radixsort_tmp/{prefix}.txt")
        prefix2file[str(prefix)] = open(chunk, "w")
    v = sys.version_info
    version = f"{v.major}.{v.minor}.{v.micro}"
    print(f"Python {version}. Start splitting...")
    t0 = time.time()
    chunk_data(big_filepath, prefix2file)
    t1 = time.time()
    print("Time for Chunking: {:0.1f}s (Python {})".format(t1 - t0, version))


def chunk_data(big_filepath, prefix2file):
    with open(big_filepath) as fp:
        for line in fp:
            prefix2file[line[:2]].write(line)


if __name__ == "__main__":
    main("numbers.txt")
