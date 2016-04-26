#!/usr/bin/env python

"""Helper script to conveniently download data."""

import wikicommons
import os


def main(db_name='category_data.db'):
    """Orchestrate it all."""
    create_database()
    cat_queue = ['Category:Images by Martin Thoma/Karlsruhe']
    import sqlite3
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    while cat_queue:
        cat = cat_queue.pop()
        file_queue = wikicommons.create_filelist(cat)
        while len(file_queue) > 0:
            filename = file_queue.pop()
            handle_file(filename['filename'])
        sql = "UPDATE categories SET done = 1 WHERE name = ?"
        c.execute(sql, (cat[len('Category:'):], ))
        conn.commit()
        sql = "SELECT name FROM categories WHERE done = 0"
        c.execute(sql)
        cat_queue = ["Category:%s" % catt[0] for catt in c.fetchall()]
    c.close()
    conn.close()


def handle_file(commons_name, db_name='category_data.db'):
    """Check if it is in DB and add if not."""
    import sqlite3
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT id FROM files WHERE name=?", (commons_name, ))
    res = c.fetchone()
    if res is None:  # File is not in the DB
        # Add the file
        details = wikicommons.get_file_details(commons_name)
        sql = "INSERT INTO files (name, url) VALUES(?, ?)"
        c.execute(sql, (commons_name, details['img_url']))
        conn.commit()
        file_id = c.lastrowid

        # Add the categories
        for cat in details['categories']:
            c.execute("SELECT id FROM categories WHERE name=?", (cat, ))
            cat_res = c.fetchone()
            if cat_res is None:
                sql = ("INSERT INTO categories (name, file_count) "
                       "VALUES (?, 1);")
                c.execute(sql, (cat, ))
                conn.commit()
                cat_id = c.lastrowid
            else:
                cat_id = cat_res[0]
            try:
                sql = ("INSERT INTO categories2files (category_id, file_id) "
                       "VALUES (?, ?)")
                c.execute(sql, (cat_id, file_id))
            except:
                pass
            conn.commit()
            # sql = ("UPDATE categories SET file_count = file_count + 1 "
            #        "WHERE id = ?", (cat_id, ))
            # c.execute(sql)
            # conn.commit()
    c.close()
    conn.close()


def create_database(db_name='category_data.db'):
    """Create db for fast lookup of category intersections."""
    import sqlite3
    if os.path.isfile(db_name):
        return
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS `categories` (
      `id` INTEGER PRIMARY KEY,
      `name` varchar(512) NOT NULL,
      `file_count` int(10) DEFAULT 0,
      `done` int(1) DEFAULT 0
    );"""
    c.execute(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS `files` (
      `id` INTEGER PRIMARY KEY,
      `name` varchar(512) NOT NULL,
      `url` varchar(1024) NOT NULL
    );"""
    c.execute(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS `categories2files` (
      `category_id` int(11) NOT NULL,
      `file_id` int(11) NOT NULL,
      PRIMARY KEY (`category_id`,`file_id`)
    );"""
    c.execute(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS `subcats` (
      `category_id` int(11) NOT NULL,
      `subcategory_id` int(11) NOT NULL,
      PRIMARY KEY (`category_id`,`subcategory_id`)
    );"""
    c.execute(sql)


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main()
