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


class Orchestrator:
    def __init__(self, state_filepath: str):
        self.state_filepath = state_filepath
        self.tasks = []
        self.read()
        if not "finished_tasks" in self.state:
            self.state["finished_tasks"] = []
            self.state["task_return_values"] = []
        if "target" not in self.state:
            self.state["target"] = os.path.abspath("out.txt")
        if "meta" not in self.state:
            self.state["meta"] = {}  # stage => time

    def read(self):
        if not os.path.isfile(self.state_filepath):
            self.state = {}
            return
        with open(self.state_filepath):
            with open(state_filepath) as fp:
                state = json.loads(fp.read())
            self.state = state

    def write(self):
        state = self.state
        state["filepath"] = self.state_filepath
        with open(state["filepath"], "w") as fp:
            fp.write(json.dumps(state))

    def completed_task(
        self, task_name: str, execution_time: float, task_return: Dict[str, Any]
    ):
        self.state["meta"][task_name] = execution_time
        self.state["finished_tasks"].append(task_name)
        self.state["task_return_values"].append(task_return)
        print(f"Time for {task_name}: {execution_time:0.1f}s")
        self.write()

    def is_completed(self, task_name):
        return task_name in self.state["finished_tasks"]

    def run(self):
        for i, task in enumerate(self.tasks):
            if self.is_completed(task.name):
                continue
            t0 = time.time()
            return_val = task.runnable(**self.state["task_return_values"][-1])
            self.state["task_return_values"].append(return_val)
            t1 = time.time()
            task_time = t1 - t0
            self.completed_task(task.name, task_time, return_val)


class Task:
    def __init__(self, name, runnable):
        self.name = name
        self.runnable = runnable


class TaskGroup(Task):
    def __init__(self, name, runnable):
        """The runnable needs to return a list of Tasks."""
        self.name = name
        self.runnable_generator = runnable

    def runnable(self, **kwargs):
        tasks = runnable_generator(**kwargs)
        return_values = {}
        for task in tasks:
            return_values[task.name] = task.run()
        return return_values


def main(big_filepath: str):
    state_filepath = os.path.abspath(".radixsort.state.json")
    orchestrator = Orchestrator(state_filepath)
    if len(orchestrator.state["task_return_values"]) == 0:
        orchestrator.state["task_return_values"].append({"big_filepath": big_filepath})
    orchestrator.tasks.append(Task("chunk_data", chunk_data))
    orchestrator.tasks.append(Task("sort_chunks", sort_chunks))
    orchestrator.tasks.append(Task("merge_data", merge_chunks))
    orchestrator.run()
    print("Done!")


def get_prefixes() -> List[str]:
    """Those are the characters the number starts with."""
    return [str(i) for i in range(10, 100)]


def chunk_data(big_filepath: str):
    """
    Sort the numbers into files which are roughly 216MB big.

    Each file is defined by its prefix.

    This takes 305,29s on my machine.
    """
    # Generate prefixes
    target_dir = "radixsort_tmp"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    prefixes = get_prefixes()

    # Chunk the data
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
    return {"chunks_to_sort": chunks_to_sort, "chunks_to_merge": chunks_to_sort[:]}


def sort_chunks(chunks_to_sort) -> Dict[str, Any]:
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
