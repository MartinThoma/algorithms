"""
Sort a huge file:

1. **Chunking**: Generate 90 chunks for all of the 2-letter prefixes (10, 11,
   12, ... 97, 98, 99). Each chunk is now small enough to fit into memory.
2. **Chunk sorting**: Sort each chunk individually.
3. **Combining**: Combine all of the chunks. As they were created by prefixes,
   this is just simply pasting the files together in the order of the prefixes.
"""
import json
import logging
import math
import os
import sys
import time
from typing import Any, Dict, List, Tuple

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


def main(big_filepath: str):
    state_filepath = os.path.abspath(".radixsort.state.json")
    if not os.path.isfile(state_filepath):
        with open(state_filepath, "w") as fp:
            fp.write(json.dumps({"finished_stages": ["setup"]}))
    state = get_state(state_filepath)
    state["filepath"] = state_filepath
    if "target" not in state:
        state["target"] = os.path.abspath("out.txt")
    if "meta" not in state:
        state["meta"] = {}  # stage => time
    if "chunk_data" not in state["finished_stages"]:
        t0 = time.time()
        target_dir = "radixsort_tmp"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        prefixes = get_prefixes()
        state = chunk_data(state, big_filepath, prefixes)
        t1 = time.time()
        state["meta"]["chunk_data"] = t1 - t0
        print(f"Time for Chunking: {t1 - t0:0.1f}s")
        write_state(state["filepath"], state)
    if "sort_chunks" not in state["finished_stages"]:
        t0 = time.time()
        state = sort_chunks(state)
        t1 = time.time()
        state["meta"]["sort_chunks"] = t1 - t0
        print(f"Sort chunks: {t1 - t0:0.1f}s")
        state["finished_stages"].append("sort_chunks")
        write_state(state["filepath"], state)
    if "merge_data" not in state["finished_stages"]:
        t0 = time.time()
        state = merge_chunks(state)
        t1 = time.time()
        state["meta"]["merge_data"] = t1 - t0
        print(f"Merged chunks: {t1 - t0:0.1f}s")
        state["finished_stages"].append("merge_data")
        write_state(state["filepath"], state)
    print("Done!")


def get_state(state_filepath: str) -> Dict[str, Any]:
    with open(state_filepath) as fp:
        state = json.loads(fp.read())
    return state


def write_state(state_filepath: str, state: Dict[str, Any]):
    with open(state_filepath, "w") as fp:
        fp.write(json.dumps(state))


def get_range(big_filepath: str) -> Tuple[str, str, int]:
    min_val, max_val = None, None
    i = 0
    with open(big_filepath) as fp:
        line = fp.readline()
        min_val = line.strip()
        max_val = line.strip()
        for line in fp:
            if i % 10_000_000 == 0:
                logger.info(f"    i={i:,}")
            line = line.strip()
            min_val = min(min_val, line)
            max_val = max(max_val, line)
            i += 1
    return min_val, max_val, i


def get_prefixes() -> List[str]:
    """Those are the characters the number starts with."""
    return [str(i) for i in range(10, 100)]


def chunk_data(state: Dict[str, Any], big_filepath: str, prefixes: List[str]):
    """
    Sort the numbers into files which are roughly 216MB big.

    Each file is defined by its prefix.

    This takes 305,29s on my machine.
    """
    prefix2file = {}
    chunks_to_sort = []
    for prefix in prefixes:
        chunk = os.path.abspath(f"radixsort_tmp/{prefix}.txt")
        chunks_to_sort.append(chunk)
        prefix2file[prefix] = open(chunk, "w")
    logger.info("Generated files")
    logger.info("Start splitting...")
    with open(big_filepath) as fp:
        for line in fp:
            prefix2file[line[:2]].write(line)
    logger.info("Done splitting...")
    state["finished_stages"].append("chunk_data")
    state["chunks_to_sort"] = chunks_to_sort
    state["chunks_to_merge"] = chunks_to_sort[:]
    return state


def sort_chunks(state: Dict[str, Any]) -> Dict[str, Any]:
    while state["chunks_to_sort"]:
        chunk_path = state["chunks_to_sort"].pop()
        t0 = time.time()
        sort_chunk(chunk_path)
        t1 = time.time()
        state["meta"][f"sorted_{chunk_path}"] = t1 - t0
        print(f"Sorted {chunk_path}: {t1 - t0:0.1f}s")
        write_state(state["filepath"], state)
    return state


def sort_chunk(chunk_path: str):
    """Reading, sorting, writing... takes about 8-10s per 216MB."""
    with open(chunk_path) as fp:
        lines = fp.readlines()
    lines = sorted(lines)
    with open(chunk_path, "w") as fp:
        fp.writelines(lines)


def merge_chunks(state: Dict[str, Any]):
    state["chunks_to_merge"] = sorted(state["chunks_to_merge"])
    state["written_lines"] = 0
    write_state(state["filepath"], state)
    with open(state["target"], "w") as fp:
        t0 = time.time()
        while state["chunks_to_merge"]:
            chunk_filepath = state["chunks_to_merge"].pop(0)
            with open(chunk_filepath) as read_fp:
                lines = read_fp.readlines()
            fp.writelines(lines)
            state["written_lines"] += len(lines)
        t1 = time.time()
        print(f"Written {chunk_filepath}: {t1 - t0:0.1f}")
        write_state(state["filepath"], state)
    return state


if __name__ == "__main__":
    main("numbers-large.txt")
