#!/usr/bin/env python3

"""Analyze the package names of PyPI."""

import json
import logging
import sys
import sqlite3
import random
from typing import Any

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_package_names(mysql: dict[str, str]) -> list[dict[str, str]]:
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    sql = "SELECT id, name FROM `packages`"
    cursor.execute(sql)
    packages = cursor.fetchall()
    return packages


def build_prefix_tree(pkg_names: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    prefix_tree = {}
    for pkg in pkg_names:
        current_node = prefix_tree
        for char in pkg["name"]:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]
        current_node["package"] = True
    return prefix_tree


def prefix_analysis(pkg_names: list[dict[str, str]], known_prefixes=None):
    pkg_names_only = [pkg["name"].lower() for pkg in pkg_names]
    if known_prefixes is None:
        known_prefixes = [
            "odoo",
            "collab",
            "conan",
            "nester",  # this might be in a head first tutorial?
            "bane",  # security stuff
            "aio",
            "asyncio",
            "tornado",
            "torch",
            "pip",
            "jupyter",
            "micropython",
            "docker",
            "sentry",
            "pandas",
            "redis",
            "robotframework",
            "graphene",
            # Machine learning
            "tensorflow",
            "keras",
            "scikit",
            "scipy",
            "numpy",
            "sklearn",
            "pytorch",
            # Common cause
            "markdown",
            "json",
            "sql",
            "pdf",
            # Web frameworks
            "dash",
            "streamlit",
            "django-cms",
            "wagtail",
            "mezzanine",
            "kotti",
            "feincms",
            "plone",
            "collective",  # plone
            "flask",
            "pydantic",
            "django",
            "fastapi",
            "bottle",
            # Testing
            "pytest",
            "flake8",
            "mypy",
            "types",
            # Companies
            "aws",
            "boto",
            "alibaba",
            "google",
            "gcp",
            "microsoft",
            "azure",
            "discord",
            "slack",
        ]
    vague_prefixes = [
        "example-pkg",
        "hello",
        "config",
        "deep",
        "meta",
        "cloud",
        "web",
        "open",
        "cli",
        "test",
        "distributions",
        "data",
        "simple",
        "easy",
        "collective",
        "auto",
        "lib",
        "example",
        "app",
    ]
    prefix_tree = build_prefix_tree(pkg_names)

    # Now traverse tree - if a 'package' node is not a leaf, then this is a
    # prefix
    i = 1
    short_packages = set()
    is_prefix_of = {}
    prefixed_by = {}
    for pkg in pkg_names:
        current_node = prefix_tree
        current_str = ""
        prefix_msgs = []
        for char in pkg["name"]:
            current_str += char
            current_node = current_node[char]
            if "package" in current_node and current_str != pkg["name"]:
                if len(current_str) <= 2:
                    short_packages.add(current_str)
                else:
                    msg = {"prefix": current_str, "long": pkg["name"]}
                    if current_str in is_prefix_of:
                        is_prefix_of[current_str].append(pkg["name"])
                    else:
                        is_prefix_of[current_str] = [pkg["name"]]
                    if pkg["name"] in prefixed_by:
                        prefixed_by[pkg["name"]].append(current_str)
                    else:
                        prefixed_by[pkg["name"]] = [current_str]
                    prefix_msgs.append(msg)
        # if len(prefix_msgs) > 0 and len(current_node) == 1:
        #     for msg in prefix_msgs:
        #         msg = ("'%s' is prefix of '%s'." %
        #                (msg['prefix'], msg['long']))
        #         print("%i. %s" % (i, msg))
        #         i += 1

    # List[Tuple[package_name, packages prefixed by this]]
    is_prefix_top = [(pkg, len(pkg_list)) for pkg, pkg_list in is_prefix_of.items()]
    is_prefix_top_dict = {
        pkg.lower(): pkg_list for pkg, pkg_list in is_prefix_of.items()
    }
    is_prefix_top = sorted(is_prefix_top, reverse=True, key=lambda n: n[1])
    print("## Packages which are prefixes of many packages:")
    found = 0
    i = 0
    while found < 50:
        isptop = is_prefix_top[i]
        i += 1
        if (
            isptop[0].startswith("py")
            or isptop[0] in known_prefixes
            or any(
                prefixpart.startswith(isptop[0].lower())
                for prefixpart in vague_prefixes + known_prefixes
            )
        ):
            continue
        found += 1
        print(
            f"{found}. {isptop[0]}: {isptop[1]} ({random.sample(is_prefix_top_dict[isptop[0].lower()], 10)})"
        )

    # Print the known ecosystems size
    knowns = sorted(
        [
            (
                pkg_name,
                [candidate for candidate in pkg_names_only if pkg_name in candidate],
            )
            for pkg_name in known_prefixes
        ],
        key=lambda n: len(n[1]),
        reverse=True,
    )
    for pkg_name, prefixed_packages in knowns:
        print(f"{len(prefixed_packages):>6,} packages contain '{pkg_name}'")

    prefixed_by_top = [(pkg, len(pkg_list)) for pkg, pkg_list in prefixed_by.items()]
    prefixed_by_top = sorted(prefixed_by_top, reverse=True, key=lambda n: n[1])
    print("## Packages which prefixed by packages:")
    for i, isptop in enumerate(prefixed_by_top[:10], start=1):
        print("%i. %s: %i" % (i, isptop[0], isptop[1]))

    print("## Short package names: %i" % len(short_packages))


def main():
    """Orchestrate the package name analysis."""
    logging.info("Get package names...")
    with open("secret.json") as f:
        mysql = json.load(f)

    pkg_names = get_package_names(mysql)
    prefix_analysis(pkg_names)
    # for package_name_link, package_name in package_names:
    #     handle_package(package_name_link, package_name, mysql)


if __name__ == "__main__":
    main()
