# Core Library modules
import json
import os
from typing import List

# Third party modules
import requests
from lxml import html


def find_packages() -> List[str]:
    response = requests.get("https://pypi.org/simple/")
    tree = html.fromstring(response.content)
    package_list = [package for package in tree.xpath("//a/text()")]

    for pkg in package_list:
        get_project_details(pkg)

    packages = [(pkg, get_project_details(pkg)) for pkg in package_list]
    packages = [
        pkg
        for pkg, details in packages
        if details["info"]["summary"] != "A package to prevent exploit"
        and has_flake8_classifier(details)
    ]
    return packages


def has_flake8_classifier(pkg_info):
    return "Framework :: Flake8" in pkg_info.get("info", {}).get("classifiers", [])


def get_project_details(package):
    filepath = os.path.join("pkg-meta", f"{package}.json")
    if os.path.isfile(filepath):
        with open(filepath) as f:
            return json.loads(f.read())
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        details = response.json()
        with open(filepath, "w") as f:
            f.write(json.dumps(details))
    except:
        print(f"Failed to get details of {package}")
        details = {"info": {"summary": ""}}
        with open(filepath, "w") as f:
            f.write(json.dumps("FAILED_DOWNLOAD"))
    return details


if __name__ == "__main__":
    # print(json.dumps(get_project_details("flake82020"), indent=4))
    packages = find_packages()
    print(f"Found {len(packages)} packages")
    for pkg in packages:
        print(pkg)
