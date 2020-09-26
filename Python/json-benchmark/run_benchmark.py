import json
import os
import timeit

import numpy as np
import orjson
import rapidjson  # python-rapidjson
import seaborn
import simdjson  # pysimdjson
import simplejson
import ujson

json_to_write = None


def read_file(filepath: str):
    with open(filepath) as fp:
        return fp.read()


def write_file(filepath, data):
    with open(filepath, "w") as fp:
        fp.write(json_to_write)


def read_json(filepath: str):
    with open(filepath) as fp:
        return json.load(fp)


def write_json(filepath: str, data):
    with open(filepath, "w") as fp:
        return json.dump(data, fp)


def read_simplejson(filepath: str):
    with open(filepath) as fp:
        return simplejson.load(fp)


def write_simplejson(filepath: str, data):
    with open(filepath, "w") as fp:
        return simplejson.dump(data, fp)


def read_ujson(filepath: str):
    with open(filepath) as fp:
        return ujson.load(fp)


def write_ujson(filepath: str, data):
    with open(filepath, "w") as fp:
        return ujson.dump(data, fp)


def read_orjson(filepath: str):
    with open(filepath) as fp:
        data = fp.read()
        return orjson.loads(data)


def write_orjson(filepath: str, data):
    with open(filepath, "wb") as fp:
        return fp.write(orjson.dumps(data))


def read_simdjson(filepath: str):
    with open(filepath) as fp:
        return simdjson.load(fp)


def write_simdjson(filepath: str, data):
    with open(filepath, "w") as fp:
        return simdjson.dump(data, fp)


def read_rapidjson(filepath: str):
    with open(filepath) as fp:
        return rapidjson.load(fp)


def write_rapidjson(filepath: str, data):
    with open(filepath, "w") as fp:
        return rapidjson.dump(data, fp)


def test_write(in_filepath: str, out_filepath: str, title: str, repetitions: int):
    filepath = os.path.abspath(in_filepath)
    print(f"File size: {os.path.getsize(filepath):,} Byte")
    data = read_json(filepath)
    globals()["json_to_write"] = json.dumps(data)
    functions = [
        (write_file, "baseline"),
        (write_json, "json"),
        (write_simplejson, "simplejson"),
        (write_ujson, "ujson"),
        (write_orjson, "orjson"),
        (write_simdjson, "simdjson"),
        (write_rapidjson, "rapidjson"),
    ]
    duration_list = {}
    for func, name in functions:
        durations = timeit.repeat(
            lambda: func("test_out.json", data), repeat=repetitions, number=1
        )
        duration_list[name] = durations
        print(
            "{func:<20}: "
            "min: {min:3.0f}ms, mean: {mean:3.0f}ms, max: {max:3.0f}ms".format(
                func=name,
                min=min(durations) * 1000,
                mean=np.mean(durations) * 1000,
                max=max(durations) * 1000,
            )
        )
        create_boxplot(duration_list, title, out_filepath)


def test_read(in_filepath: str, out_filepath: str, title: str, repetitions: int):
    filepath = os.path.abspath(in_filepath)
    print(f"## {title}")
    print(f"File size: {os.path.getsize(filepath):,} Byte")
    ground_truth = read_json(filepath)
    functions = [
        (read_file, "baseline"),
        (read_json, "json"),
        (read_simplejson, "simplejson"),
        (read_ujson, "ujson"),
        (read_orjson, "orjson"),
        (read_simdjson, "simdjson"),
        (read_rapidjson, "rapidjson"),
    ]
    duration_list = {}
    for func, name in functions:
        is_correct = func(filepath) == ground_truth
        if is_correct:
            correctness = "CORRECT"
        else:
            correctness = "INCORRECT!!!"
        durations = timeit.repeat(lambda: func(filepath), repeat=repetitions, number=1)
        duration_list[name] = durations
        print(
            "{func:<20}: {correctness}, "
            "min: {min:3.0f}ms, mean: {mean:3.0f}ms, max: {max:3.0f}ms".format(
                func=name,
                min=min(durations) * 1000,
                correctness=correctness,
                mean=np.mean(durations) * 1000,
                max=max(durations) * 1000,
            )
        )
        create_boxplot(duration_list, title, out_filepath)


def create_boxplot(duration_list, title, out_filepath, sort_order=False):
    import operator

    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(num=None, figsize=(8, 4), dpi=300, facecolor="w", edgecolor="k")
    sns.set(style="whitegrid")
    if sort_order:
        sorted_keys, sorted_vals = zip(
            *sorted(duration_list.items(), key=operator.itemgetter(1))
        )
    else:
        sorted_keys, sorted_vals = zip(*duration_list.items())
    flierprops = dict(markerfacecolor="0.75", markersize=1, linestyle="none")
    ax = sns.boxplot(data=sorted_vals, width=0.3, orient="h", flierprops=flierprops,)
    ax.set_title(title)
    ax.set(xlabel="Time in s", ylabel="")
    plt.yticks(plt.yticks()[0], sorted_keys)
    plt.tight_layout()
    plt.savefig(out_filepath)


if __name__ == "__main__":
    repetitions = 1000
    test_read(
        "data/canada.json",
        "read-geojson.png",
        f"2.1 MB GeoJSON - Read Speed over {repetitions} repetitions",
        repetitions
    )
    test_write(
        "data/canada.json",
        "write-geojson.png",
        f"2.1 MB GeoJSON - Write Speed over {repetitions} repetitions",
        repetitions
    )
    test_read(
        "data/twitter.json",
        "read-twitter.png",
        f"630 KB Twitter JSON - Read Speed over {repetitions} repetitions",
        repetitions
    )
    test_write(
        "data/twitter.json",
        "write-twitter.png",
        f"630 KB Twitter JSON - Write Speed over {repetitions} repetitions",
        repetitions
    )
    test_read(
        "data/floats.json",
        "read-float.png",
        f"2 MB Float JSON - Read Speed over {repetitions} repetitions",
        repetitions
    )
    test_write(
        "data/floats.json",
        "write-float.png",
        f"2 MB Float JSON - Write Speed over {repetitions} repetitions",
        repetitions
    )
