#!/usr/bin/env python

"""Analyze a history file."""

import datetime
import re

import click
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd
import yaml


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--shell", type=click.Choice({"zsh", "fish", "bash"}))
def cli(filename: str, shell: str):
    main(filename, shell)


def main(filename: str, shell: str, apply_grouping: bool = True) -> pd.DataFrame:
    with open(filename) as f:
        content = f.read()
    df = extract_command_list(content, shell=shell)
    df["cleaned_command"] = df["command"]
    df = prefix_removal(df, prefix="sudo")
    df = prefix_removal(df, prefix="time")
    new = df["cleaned_command"].str.split(" ", expand=True)
    df["base_command"] = new[0]

    if apply_grouping:
        with open("grouping.yaml") as f:
            grouping = yaml.safe_load(f)
        grouping_t = {}
        for to, from_list in grouping.items():
            for from_str in from_list:
                grouping_t[from_str] = to
        df["base_command"] = df["base_command"].map(lambda n: grouping_t.get(n, n))

    counts = df.base_command.value_counts()
    min_occurences = 20
    if max(counts) < min_occurences:
        min_occurences = max(max(counts) - 10, min(counts))
    counts = counts[counts >= min_occurences]
    print(counts)
    min_date = min(df["date"])
    max_date = max(df["date"])
    plt.title(
        f"Command distribution from {min_date:%Y-%m-%d} "
        f"to {max_date:%Y-%m-%d}\nmin occurences = {min_occurences}"
    )
    ax = counts.plot(kind="pie", figsize=(8, 8), title="")
    ax.set_ylabel("")
    print(df)
    plt.savefig("history.png")
    return df


def extract_command_list(content: str, shell: str) -> pd.DataFrame:
    commands = []
    lines = content.rstrip().split("\n")
    # This is the ZSH history result pattern:
    #                9      13.5.2018 10:11  cd fonts
    # You might need to adjust the pattern!
    if shell == "zsh":
        pattern = (
            r"\s+(?P<number>\d+)\s+(?P<date>\d+\.\d+\.\d+ \d+:\d+)\s+(?P<command>.+)"
        )
    elif shell == "bash":
        pattern = r"\s+(?P<number>\d+)\s+(?P<command>.+)"
    else:
        pattern = r"(?P<command>.+)"

    for line in lines:
        re_result = re.search(pattern, line, re.IGNORECASE)
        if re_result is None:
            continue
        groups = re_result.groupdict()
        commands.append(
            (
                groups.get("number", None),
                dateutil.parser.parse(groups.get("date", "1970-01-01")),
                groups.get("command", None),
            )
        )
    df = pd.DataFrame(commands, columns=["number", "date", "command"])
    return df


def clean_prefix(x: str, prefix: str) -> str:
    """Remove a prefix and all options from the command x."""
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


def prefix_removal(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """
    Annotate commands which have the given prefix and remove it from cleaned_command.

    Parameters
    ----------
    df : pd.DataFrame
    prefix : str

    Returns
    -------
    df : pd.DataFrame
    """
    df[prefix] = df["cleaned_command"].str.startswith(f"{prefix} ")
    df["cleaned_command"] = df["cleaned_command"].map(
        lambda x: clean_prefix(x, prefix=prefix)
    )
    return df


if __name__ == "__main__":
    cli()
