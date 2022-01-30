from analyze_downloaded_gems import dict_factory, get_non_crap
import sqlite3
from build_datastructure import get_package_info, insert_release
from packaging import version
from typing import Any, Dict


def main():
    non_crap = get_non_crap()
    print(f"Non-crap packages: {len(non_crap):,}")
    pkg2max_version = {}
    for pkg in non_crap:
        pkg2max_version[pkg] = get_latest_release(pkg)
        if pkg2max_version[pkg] is None:
            get_and_insert_release(pkg)


def get_latest_release(pkg_name: str) -> Dict[str, Any]:
    conn = sqlite3.connect("pypi.db")
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"SELECT id FROM packages WHERE name='{pkg_name}'")
    row = c.fetchone()
    pkg_id = row["id"]
    c.execute(f"SELECT * FROM releases WHERE package_id='{pkg_id}'")
    rows = c.fetchall()
    latest_release = None
    max_release_number = version.parse("0-dev")
    for row in rows:
        release_number = version.parse(row["release_number"])
        if release_number > max_release_number:
            max_release_number = release_number
            latest_release = row
    return latest_release


def get_and_insert_release(pkg_name: str):
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM packages WHERE name='{pkg_name}'")
    row = cursor.fetchone()
    db_package_id = row["id"]

    package_info = get_package_info(pkg_name)
    if package_info is None:
        print(f"!!!! Could not find info for '{pkg_name}'")
        return
    releases = package_info.releases
    insert_count = 0
    for release_number, release_all in releases.items():
        for release in release_all:
            insert_release(cursor, db_package_id, release, release_number)
            insert_count += 1
            connection.commit()
    cursor.close()
    connection.close()
    print(f"Inserted {insert_count:,} releases for {pkg_name}")


if __name__ == "__main__":
    main()
