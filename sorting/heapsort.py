# Core Library modules
import datetime
import heapq
import json
import os
import time
from tempfile import mkstemp
from typing import List


def main(numbers_filepath):
    # Split files: 2184s = 36min 24s
    splitting_success_marker = os.path.abspath("heapsort_temp/.splitting_done")
    if not os.path.isfile(splitting_success_marker):
        filepaths = split(numbers_filepath)
        with open(splitting_success_marker, "w") as f:
            f.write(json.dumps(filepaths))
    else:
        with open(splitting_success_marker) as f:
            filepaths = json.loads(f.read())
        print(f"Restored filepaths: {filepaths}")

    # Merges: 8661s = 144min 21s
    cleanup(os.path.abspath("heapsort_temp/"), filepaths)
    result_path = merge_all(filepaths, splitting_success_marker)
    print(f"Sorted result is in {result_path}")


def get_bool(text: str) -> bool:
    data = "placeholder"
    yes = ["y", "yes", "true", "1"]
    no = ["n", "no", "false", "0"]
    while data.lower() not in yes + no:
        data = input(text)
    return data in yes


def cleanup(directory: str, filepaths: List[str]) -> List[str]:
    potential = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]
    no_delete = set(filepaths)
    no_delete.add(os.path.join(directory, ".splitting_done"))
    for filepath in potential:
        if filepath not in no_delete:
            delete = get_bool(f"Do you want to remove {filepath}? [y/n] ")
            if delete:
                os.remove(filepath)
                print(f"Removed {filepath}")


def split(numbers_filepath: str) -> List[str]:
    tmp_dir_path = os.path.abspath("heapsort_temp")
    if not os.path.isdir(tmp_dir_path):
        os.mkdir(tmp_dir_path)

    breaker = 10 ** 7
    filepaths: List[str] = []

    with open(numbers_filepath) as f:
        filepath = os.path.join(tmp_dir_path, f"{breaker}-{len(filepaths)}.txt")
        next_break = breaker
        to_sort: List[str] = []
        breaks = 0
        for index, line in enumerate(f):
            # Make sure the program can be interrupted
            if os.path.isfile(filepath):
                if index % breaker == 1:
                    print(f"Found {filepath}. Skipping...")
                if index == next_break:
                    filepaths.append(filepath)
                    filepath = os.path.join(
                        tmp_dir_path, f"{breaker}-{len(filepaths)}.txt"
                    )
                    print(f"Next filepath: {filepath}")
                    next_break += breaker
                continue

            if index == next_break:
                # Split workload
                to_sort = sorted(to_sort)
                filepaths.append(filepath)
                write_data(filepath, to_sort)

                next_break += breaker
                filepath = os.path.join(tmp_dir_path, f"{breaker}-{len(filepaths)}.txt")
                print(f"Next filepath: {filepath}")
                to_sort = []
            to_sort.append(line)
        # Remainders - same as in the previous if-condition
        if len(to_sort) > 0:
            # Split workload
            to_sort = sorted(to_sort)
            filepaths.append(filepath)
            write_data(filepath, to_sort)
    return filepaths


# 1303
def merge_all(filepaths: List[str], filepaths_filename: str) -> str:
    while len(filepaths) >= 2:
        t0 = time.time()
        filepath1 = filepaths.pop()
        filepath2 = filepaths.pop()
        _, target_path = mkstemp(
            prefix="heapsort-", suffix=".txt", dir=os.path.dirname(filepaths_filename)
        )
        os.close(_)
        merge_files(filepath1, filepath2, target_path)

        # The order here is important! Make sure that you can continue if the
        # program crashes or is interrupted!
        # So: First merge, then write this file
        filepaths.append(target_path)
        with open(filepaths_filename, "w") as f:
            f.write(json.dumps(filepaths))

        # Now cleanup is save
        os.remove(filepath1)
        os.remove(filepath2)
        t1 = time.time()
        print(f"Merged two files in {t1 - t0:0.2f}s. Remaining: {len(filepaths)}")
    return filepaths[0]


def write_data(filepath, data):
    with open(filepath, "w") as f:
        for line in data:
            f.write(line)


def read_data(filepath):
    # 68s just to read the file!
    last_line = None
    t0 = time.time()
    with open(filepath) as f:
        for line in f:
            last_line = line
    t1 = time.time()
    print(f"Read file in {t1 - t0:.1f}s")
    return last_line


def merge_files(filepath1: str, filepath2: str, outpath: str) -> int:
    # https://docs.python.org/2/library/heapq.html#heapq.merge
    with open(outpath, "w") as fout, open(filepath1) as f1, open(filepath2) as f2:
        for line in heapq.merge(f1, f2):
            fout.write(line)


if __name__ == "__main__":
    filepath = os.path.abspath("numbers-large.txt")
    main(filepath)
