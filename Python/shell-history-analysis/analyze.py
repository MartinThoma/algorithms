#!/usr/bin/env python

"""Analyze a history file"""

import re

import click
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def cli(filename):
    main(filename)


def main(filename: str):
    with open(filename) as f:
        content = f.read()
    df = extract_command_list(content)
    df["cleaned_command"] = df["command"]
    df = prefix_removal(df, prefix="sudo")
    df = prefix_removal(df, prefix="time")
    new = df["cleaned_command"].str.split(" ", expand=True)
    df["base_command"] = new[0]
    print(df.base_command.value_counts())
    counts = df.base_command.value_counts()
    print(counts)
    min_occurences = 30
    counts = counts[counts >= min_occurences]
    plt.title(
        f"Command distribution from {min(df['date']):%Y-%m-%d} to {max(df['date']):%Y-%m-%d}\nmin occurences = {min_occurences}"
    )
    ax = counts.plot(kind="pie", figsize=(8, 8), title="")
    ax.set_ylabel("")
    print(df)
    plt.savefig("history.png")
    return df


def extract_command_list(content: str) -> pd.DataFrame:
    commands = []
    lines = content.rstrip().split("\n")
    #                9      13.5.2018 10:11  cd fonts
    pattern = r"\s+(\d+)\s+(\d+\.\d+\.\d+ \d+:\d+)\s+(.+)"
    for line in lines:
        re_result = re.search(pattern, line, re.IGNORECASE)
        if re_result is None:
            continue
        commands.append(
            (
                re_result.group(1),
                dateutil.parser.parse(re_result.group(2)),
                re_result.group(3),
            )
        )
    df = pd.DataFrame(commands, columns=["number", "date", "command"])
    return df


def clean_prefix(x, prefix):
    if not x.startswith(prefix):
        return x
    x = x[len(prefix) :]
    i = 0
    last_was_minus = False
    for i, char in enumerate(x):
        if last_was_minus:
            if char == " ":
                last_was_minus = False
        if char == "-":
            last_was_minus = True
        if char not in ["-", " "] and not last_was_minus:
            break
    x = x[i:]
    return x


def prefix_removal(df: pd.DataFrame, prefix: str):
    """Annotate which commands had "sudo" as a prefix and add a "cleaned" command."""
    df[prefix] = df["cleaned_command"].str.startswith(f"{prefix} ")
    df["cleaned_command"] = df["cleaned_command"].map(
        lambda x: clean_prefix(x, prefix=prefix)
    )
    # df.loc[df[prefix], 'cleaned_command'] = df[df[prefix]]['cleaned_command'].str.slice(start=len(prefix) + 1)
    # df.loc[~df[prefix], 'cleaned_command'] = df[~df[prefix]]['cleaned_command']
    return df


if __name__ == "__main__":
    cli()
