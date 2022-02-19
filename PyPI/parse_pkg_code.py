import glob
from pathlib import Path
from tqdm import tqdm
import os
from tempfile import mkdtemp
import shutil
from typing import List, Optional, Dict
import tarfile
from zipfile import ZipFile
import sqlite3
from analyze_downloaded_gems import standardize_name, get_pkg_name_from_path
import uuid
from itertools import takewhile, repeat
import pickle


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class State:
    def __init__(
        self,
        storage_path: Path,
        pkgs: List[str],
        pkg2id: Dict[str, str],
        pkg_id2release_id: Dict[str, str],
    ):
        self.storage_path = storage_path
        self.pkgs = pkgs
        self.pkg2id = pkg2id
        self.pkg_id2release_id = pkg_id2release_id
        self.done = set()

    def save(self):
        with open(self.storage_path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def create(cls, storage_path: Path, pkg_path: Path) -> "State":
        pkgs = sorted(glob.glob(f"{pkg_path}/*"))

        conn = sqlite3.connect("pypi.db")
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(f"SELECT id, name FROM packages")
        rows = c.fetchall()
        pkg_id2pkg = {row["id"]: row for row in rows}
        pkg2id = {
            standardize_name(pkg["name"]): pkg_id for pkg_id, pkg in pkg_id2pkg.items()
        }
        c.execute(f"SELECT package_id, latest_release_id FROM computed_values")
        rows = c.fetchall()
        pkg_id2release_id = {
            row["package_id"]: row["latest_release_id"] for row in rows
        }
        return State(storage_path, pkgs, pkg2id, pkg_id2release_id)

    @classmethod
    def get(cls, pkg_path: Path, storage_path: Path) -> "State":
        if storage_path.exists() and storage_path.is_file():
            with open(storage_path, "rb") as file:
                object = pickle.load(file)
                return object
        else:
            return cls.create(storage_path, pkg_path)


class StateTracker:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.done : int = -1
        self.exceptions = 0

    def save(self):
        with open(self.storage_path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def get(cls, storage_path: Path) -> "StateTracker":
        if storage_path.exists() and storage_path.is_file():
            with open(storage_path, "rb") as file:
                object = pickle.load(file)
                return object
        else:
            return StateTracker(storage_path)

def main(path: Path):
    helpers = State.get(path, Path("parse_pkg_code_state-helpers.pickle"))
    helpers.save()
    state_tracker = StateTracker.get(Path("parse_pkg_code_state-status.pickle"))

    for i in tqdm(range(len(helpers.pkgs))):
        if i <= state_tracker.done:
            continue
        pkg = Path(helpers.pkgs[i])
        try:
            pkg_id = helpers.pkg2id.get(standardize_name(get_pkg_name_from_path(pkg)))
            if pkg_id is None:
                print(f"Couldn't find package id for {pkg}")
                continue
            release_id = helpers.pkg_id2release_id.get(pkg_id)
            handle_single_package(pkg_id, release_id, pkg)
        except Exception as e:
            state_tracker.exceptions += 1
            print(f"Got Exception for {pkg}: {e}")
        state_tracker.done = i
        state_tracker.save()


def handle_single_package(
    pkg_id: str, release_id: Optional[str], filepath: Path
) -> None:
    dirpath = extract_package(filepath)
    if dirpath is None:
        return
    filepaths = get_filepaths(Path(dirpath))
    for filepath in filepaths:
        analyze_file(pkg_id, release_id, filepath)

    # Cleanup
    shutil.rmtree(dirpath, ignore_errors=True)


def count_lines_of_file(filename):
    f = open(filename, "rb")
    bufgen = takewhile(lambda x: x, (f.raw.read(1024 * 1024) for _ in repeat(None)))
    return sum(buf.count(b"\n") for buf in bufgen)


def analyze_file(package_id: str, release_id: Optional[str], file_path: Path):
    lines = count_lines_of_file(file_path)
    file_size = file_path.stat().st_size
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    sql = "INSERT INTO package_files (id, package_id, release_id, file_path, file_name, file_extension, lines, file_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(
        sql,
        (
            str(uuid.uuid4()),
            package_id,
            release_id,
            "/".join(
                str(file_path).split("/")[3:]
            ),  # I'm only interested in the relative path
            file_path.name,
            file_path.suffix,
            lines,
            file_size,
        ),
    )
    connection.commit()
    # TODO: Lines


def extract_package(filepath: Path) -> Optional[str]:
    basename = os.path.basename(filepath)
    dirpath = mkdtemp(prefix="pypi_analysis_", suffix=basename)
    try:
        extract(str(filepath), dirpath)
    except ValueError as e:
        print(f"{filepath} has a weird format!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        shutil.rmtree(dirpath, ignore_errors=True)
        return None
    except Exception as e:
        print(f"{filepath} is not extractable ({e})")
        return None
    return dirpath


def extract(source_file: str, target_directory: str) -> None:
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


def get_filepaths(dirpath: Path) -> List[Path]:
    all_filenames = []
    # r=root, d=directories, f = files
    for root, _directories, filenames in os.walk(dirpath):
        for filename in filenames:
            all_filenames.append(Path(os.path.join(root, filename)))
    return all_filenames


if __name__ == "__main__":
    main(
        path=Path(
            "/media/moose/1d41967e-6a0c-4c0e-af8c-68d4fae7fa64/moose/pypipackages"
        )
    )
