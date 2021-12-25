#!/usr/bin/env python
import glob
import io
import os
import shutil
import tarfile
from collections import Counter
from configparser import ConfigParser
from dataclasses import dataclass
from tempfile import mkdtemp
from typing import Dict, List, Optional, Set, Tuple, Union
from zipfile import ZipFile

import progressbar
import toml


@dataclass
class PkgInfo:
    setupcfg_dict: Optional[Dict]
    pyprojecttoml_dict: Optional[Dict]
    pkg_type: str
    filenames: Counter


@dataclass
class AggregateInfo:
    total_packages: int
    with_setupcfg: int
    with_pyprojcttoml: int
    with_pyprojcttoml_and_setupcfg: int
    setupcfg: Dict[str, List[Union[int, Counter]]]
    pyprojecttoml: Dict[str, List[Union[int, Counter]]]
    pkg_types: Counter
    filenames: Counter


def aggregate_pkg_info(aggregated: AggregateInfo, pkg_info: PkgInfo) -> AggregateInfo:
    aggregated.total_packages += 1
    aggregated.pkg_types += Counter([pkg_info.pkg_type])
    aggregated.filenames += pkg_info.filenames
    if pkg_info.setupcfg_dict is not None:
        aggregated.with_setupcfg += 1
        for section in pkg_info.setupcfg_dict.keys():
            if section not in aggregated.setupcfg:
                aggregated.setupcfg[section] = [0, Counter()]
            aggregated.setupcfg[section][0] += 1
            aggregated.setupcfg[section][1] += Counter(
                list(pkg_info.setupcfg_dict[section].keys())
            )
    if pkg_info.pyprojecttoml_dict is not None:
        aggregated.with_pyprojcttoml += 1
        for section in pkg_info.pyprojecttoml_dict.keys():
            if section not in aggregated.pyprojecttoml:
                aggregated.pyprojecttoml[section] = [0, Counter()]
            aggregated.pyprojecttoml[section][0] += 1
            aggregated.pyprojecttoml[section][1] += Counter(
                list(pkg_info.pyprojecttoml_dict[section].keys())
            )
    if pkg_info.setupcfg_dict is not None and pkg_info.pyprojecttoml_dict is not None:
        aggregated.with_pyprojcttoml_and_setupcfg += 1
    return aggregated


def main(path, testrun=False):
    pkgs = sorted(glob.glob(f"{path}/*"))
    pkg_info_aggregated = AggregateInfo(
        total_packages=0,
        with_setupcfg=0,
        with_pyprojcttoml=0,
        with_pyprojcttoml_and_setupcfg=0,
        setupcfg={},
        pyprojecttoml={},
        pkg_types=Counter(),
        filenames=Counter(),
    )
    exceptions = 0
    for i in progressbar.progressbar(range(len(pkgs))):
        if testrun and i > 2000:
            break
        pkg = pkgs[i]
        try:
            pkg_info = handle_single_package(pkg)
        except Exception as e:
            exceptions += 1
            print(f"Got Exception for {pkg}: {e}")
            continue
        pkg_info_aggregated = aggregate_pkg_info(pkg_info_aggregated, pkg_info)

    print("\n## pkg types")
    for pkg_type, count in sorted(
        pkg_info_aggregated.pkg_types.items(), key=lambda n: n[1], reverse=True
    ):
        print(f"* {count:>7,}× {pkg_type}")

    print("\n### setup.cfg")
    common_sections = []
    for section, (count, _) in sorted(
        pkg_info_aggregated.setupcfg.items(), key=lambda n: n[1][0], reverse=True
    ):
        if count < 100:
            break
        common_sections.append(section)
        print(f"* {count:>7,}× {section}")
    for section in common_sections:
        print(f"#### {section}")
        for value, count in sorted(
            pkg_info_aggregated.setupcfg[section][1].items(),
            key=lambda n: n[1],
            reverse=True,
        ):
            if count < 100:
                break
            print(f"* {count:>7,}× {value}")

    print("\n### pyproject.toml")
    common_sections = []
    for section, (count, _) in sorted(
        pkg_info_aggregated.pyprojecttoml.items(), key=lambda n: n[1][0], reverse=True
    ):
        if count < 100:
            break
        common_sections.append(section)
        print(f"* {count:>7,}× {section}")

    for section in common_sections:
        print(f"#### {section}")
        for value, count in sorted(
            pkg_info_aggregated.pyprojecttoml[section][1].items(),
            key=lambda n: n[1],
            reverse=True,
        ):
            if count < 100:
                break
            print(f"* {count:>7,}× {value}")

    print(f"Count of exceptions={exceptions}")

    print("\n## Filenames")
    group_counts: Dict[
        str,
    ] = {}  # group -> [count, Dict[filename, count]]
    for filename, count in sorted(
        pkg_info_aggregated.filenames.items(), key=lambda n: n[1], reverse=True
    ):
        if count < 100 and not testrun:
            break
        group = filename2group(filename)
        if group not in group_counts:
            group_counts[group] = [0, {}]
        group_counts[group][0] += count
        group_counts[group][1][filename] = count
    for group, (count, elements) in sorted(
        group_counts.items(), key=lambda n: n[1][0], reverse=True
    ):
        if len(elements) == 1:
            print(f"* {count:>7,}× {group}")
        else:
            el_str = ", ".join(
                [
                    f"{f_count:,}× {filename}"
                    for filename, f_count in sorted(
                        elements.items(), key=lambda n: n[1], reverse=True
                    )
                    if f_count >= 100
                ]
            )
            print(f"* {count:>7,}× {group}: {el_str}")


def filename2group(filename):
    if (
        filename.lower().endswith(".po")
        or filename.lower().endswith(".mo")
        or filename.lower().endswith(".pot")
    ):
        return "Translations"
    elif filename in [
        "requires.txt",
        "SOURCES.txt",
        "dependency_links.txt",
        "entry_points.txt",
        "not-zip-safe",
        "zip-safe",
    ]:
        return "Package"
    elif filename.lower() in ["readme", "readme.md", "readme.rst", "readme.txt"]:
        return "README"
    elif filename.lower() in [
        "license",
        "license.txt",
        "license.gpl",
        "license.md",
        "license.rst",
    ]:
        return "LICENSE"
    elif "requirements" in filename.lower():
        return "requirements"
    elif "changes" in filename.lower() or "changelog" in filename.lower():
        return "CHANGES"
    elif "authors" in filename.lower():
        return "authors"
    elif (
        "intall.txt" in filename.lower()
        or "intall.rst" in filename.lower()
        or "intall.md" in filename.lower()
    ):
        return "INSTALL"
    elif "__init__" in filename:
        return "__init__"
    elif (
        filename.lower().endswith(".png")
        or filename.lower().endswith(".jpg")
        or filename.lower().endswith(".jpeg")
        or filename.lower().endswith(".gif")
        or filename.lower().endswith(".ico")
        or filename.lower().endswith(".svg")
    ):
        return "Images"
    elif (
        filename.lower().endswith(".ttf")
        or filename.lower().endswith(".woff")
        or filename.lower().endswith(".woff2")
        or filename.lower().endswith(".eot")
        or filename.lower().endswith(".otf")
    ):
        return "Font"
    elif filename.lower().endswith(".h"):
        return "C Header Files"
    elif (
        filename.lower().endswith(".c")
        or filename.lower().endswith(".cpp")
        or filename.lower().endswith(".hpp")
        or filename.lower().endswith(".hxx")
    ):
        return "C / C++ Files"
    elif filename.lower().endswith(".so"):
        return "*.so"
    elif filename.lower().endswith(".ipynb"):
        return "*.ipynb"
    elif filename.lower().endswith(".sql"):
        return "*.sql"
    elif filename.lower().endswith(".pdf"):
        return "*.pdf"
    elif filename.lower().endswith(".exe") or filename.lower().endswith(".dll"):
        return "Windows"
    elif filename.lower().endswith(".bat"):
        return "*.bat"
    elif filename.lower().endswith(".sh"):
        return "*.sh"
    elif filename.lower().endswith(".rsa"):
        return "*.rsa"  # security?
    elif filename.lower().endswith(".ini"):
        return "*.ini"
    elif filename.lower().endswith(".lua"):
        return "*.lua"
    elif filename.lower().endswith(".db"):
        return "*.db"
    elif filename.lower().endswith(".xaf"):
        return "*.xaf"
    elif filename.lower().endswith(".pdb"):
        return "*.pdb"
    elif filename.lower().endswith(".tex") or filename.lower().endswith(".sty"):
        return "TeX"
    elif filename.lower().endswith(".dat"):
        return "*.dat"
    elif filename.lower().endswith(".r"):
        return "*.r"
    elif filename.lower().endswith(".csv"):
        return "*.csv"
    elif filename.lower().endswith(".m"):
        return "*.m"
    elif filename.lower().endswith(".sif"):
        return "*.sif"
    elif filename.lower().endswith(".yml") or filename.lower().endswith(".yaml"):
        return "YAML"
    elif filename.lower().endswith(".qopml"):
        return "*.qopml"
    elif filename.lower().endswith(".pyc"):
        return "*.pyc"
    elif filename.lower().endswith(".json"):
        return "*.json"
    elif filename.lower().endswith(".jsonld"):
        return "*.jsonld"
    elif (
        filename.lower().endswith(".xml")
        or filename.lower().endswith(".xslt")
        or filename.lower().endswith(".xsl")
        or filename.lower().endswith(".dtd")
    ):
        return "*XML"
    elif filename.lower().endswith(".bst"):
        return "*.bst"
    elif filename.lower().endswith(".php"):
        return "*.php"
    elif (
        filename.lower().endswith(".zip")
        or filename.lower().endswith(".gz")
        or filename.lower().endswith(".7z")
    ):
        return "Compressed"
    elif filename.lower().endswith(".toml"):
        return "*.toml"
    elif filename.lower().endswith(".pickle"):
        return "*.pickle"
    elif (
        filename.lower().endswith(".html")
        or filename.lower().endswith(".htm")
        or filename.lower().endswith(".css")
        or filename.lower().endswith(".js")
        or filename.lower().endswith(".scss")
        or filename.lower().endswith(".less")
        or filename.lower().endswith(".htaccess")
        or filename.lower().endswith(".mako")
        or filename.lower().endswith(".tmpl")
        or filename.lower().endswith(".jinja")
    ):
        return "Web"
    else:
        return filename


def handle_single_package(filepath: str) -> PkgInfo:
    pkg_info = PkgInfo(
        setupcfg_dict=None,
        pyprojecttoml_dict=None,
        pkg_type=get_pkg_type(filepath),
        filenames=Counter(),
    )
    basename = os.path.basename(filepath)
    dirpath = mkdtemp(prefix="pypi_analysis_", suffix=basename)
    try:
        extract(filepath, dirpath)
    except ValueError as e:
        print(f"{filepath} has a weird format!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        shutil.rmtree(dirpath, ignore_errors=True)
        return pkg_info
    except:
        print(f"{filepath} is not extractable")
        return pkg_info
    subdirs = [
        os.path.join(dirpath, subdir)
        for subdir in os.listdir(dirpath)
        if os.path.isdir(os.path.join(dirpath, subdir))
    ]
    all_filenames = []
    # r=root, d=directories, f = files
    for root, directories, filenames in os.walk(dirpath):
        for filename in filenames:
            all_filenames.append(filename)
    pkg_info.filenames = Counter(all_filenames)

    # Whl has this
    subdirs = [subdir for subdir in subdirs if not subdir.endswith(".dist-info")]

    if len(subdirs) != 1:
        # print(f"{filepath} has {len(subdirs)} subdirectories: {subdirs}")
        shutil.rmtree(dirpath, ignore_errors=True)
        return pkg_info
    pkg_path = subdirs[0]
    pkg_info.setupcfg_dict = get_setup_cfg(pkg_path)
    pkg_info.pyprojecttoml_dict = get_pyprojecttoml(pkg_path)
    shutil.rmtree(dirpath, ignore_errors=True)
    return pkg_info


def get_setup_cfg(pkg_path):
    setup_cfg = None
    elements = [os.path.join(pkg_path, element) for element in os.listdir(pkg_path)]
    setup_cfg_path = find_setup_cfg(elements)
    if setup_cfg_path is not None:
        setup_cfg = read_setup_cfg(setup_cfg_path)
    return setup_cfg


def get_pyprojecttoml(pkg_path):
    pyprojecttoml_dict = None
    elements = [os.path.join(pkg_path, element) for element in os.listdir(pkg_path)]
    pyprojecttoml_path = find_pyprojecttoml(elements)
    if pyprojecttoml_path is not None:
        pyprojecttoml_dict = read_pyprojecttoml(pyprojecttoml_path)
    return pyprojecttoml_dict


def find_setup_cfg(filepaths):
    for filepath in filepaths:
        if os.path.isfile(filepath) and filepath.endswith("setup.cfg"):
            return filepath


def find_pyprojecttoml(filepaths):
    for filepath in filepaths:
        if os.path.isfile(filepath) and filepath.endswith("pyproject.toml"):
            return filepath


def read_setup_cfg(filepath):
    # Load the configuration file
    config = ConfigParser(allow_no_value=True)
    with open(filepath) as f:
        config.readfp(f)

    setupcfg_dict = {}

    # List all contents
    for section in config.sections():
        setupcfg_dict[section] = {}
        for options in config.options(section):
            setupcfg_dict[section][options] = config.get(section, options)
    return setupcfg_dict


def read_pyprojecttoml(filepath):
    # Load the configuration file
    with open(filepath) as f:
        toml_string = f.read()

    parsed_toml = toml.loads(toml_string)
    return parsed_toml


def extract(source_file, target_directory):
    if source_file.endswith("tar.gz"):
        tar = tarfile.open(source_file, "r:gz")
        tar.extractall(target_directory)
        tar.close()
    elif source_file.endswith("tar.bz2"):
        tar = tarfile.open(source_file, "r:bz2")
        tar.extractall(target_directory)
        tar.close()
    elif source_file.endswith("tar"):
        tar = tarfile.open(source_file, "r:")
        tar.extractall(target_directory)
        tar.close()
    elif any(source_file.endswith(ext) for ext in ["whl", "zip", "egg"]):
        with ZipFile(source_file, "r") as zip_obj:
            zip_obj.extractall(target_directory)
    else:
        raise ValueError(f"Could not extract {source_file}")


def get_pkg_type(filepath: str) -> str:
    if filepath.endswith("tar.gz"):
        return "tar.gz"
    elif filepath.endswith("tar"):
        return "tar"
    elif filepath.endswith("tar.bz2"):
        return "tar.bz2"
    elif filepath.endswith("whl"):
        return "whl"
    elif filepath.endswith("zip"):
        return "zip"
    elif filepath.endswith("egg"):
        return "egg"
    else:
        print("#" * 80)
        print(filepath)
        return "OTHER"


if __name__ == "__main__":
    main(path="pypipackages")
