"""Sort a huge amount of data by inserting it into SQLite."""

# Core Library modules
import logging
import sqlite3
import sys
import time

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


def main(big_filepath: str):
    db_filepath = "numbers-large.sqlite"
    output_filepath = "sqlite-sorted-numbers.txt"

    if True:
        t0 = time.time()
        create_db(big_filepath, db_filepath, batch_size=10 ** 7)
        t1 = time.time()
        print(f"create_db finished in {t1 - t0}")
    if True:
        t0 = time.time()
        read_sort_write(db_filepath, output_filepath)
        t1 = time.time()
        print(f"sorting and writing with sqlite finished in {t1 - t0}")


def create_db(big_filepath: str, db_filepath: str, batch_size: int = 10 ** 6):
    con = sqlite3.connect(db_filepath)

    # Create the table
    con.execute("CREATE TABLE numbers(i)")

    batch_count = 0
    with open(big_filepath) as fp:
        batch = []
        for line in fp:
            batch.append((line,))
            if len(batch) >= batch_size:
                con.executemany("INSERT INTO numbers(i) VALUES (?)", batch)
                con.commit()
                batch = []
                batch_count += 1
                logger.info(f"Finished batch {batch_count}")
        con.executemany("insert into numbers(i) values (?)", batch)
        con.commit()
        logger.info("Make index")
        con.execute("CREATE INDEX fooindex ON numbers(i)")
        con.commit()
        logger.info("Finished making index.")
        con.close()
    logger.info("Finished creation of SQLiteDB")


def read_sort_write(db_filepath: str, output_filepath: str):
    con = sqlite3.connect(db_filepath)
    res = con.execute("SELECT i FROM numbers ORDER BY i ASC")
    with open(output_filepath, "w") as fp:
        for el in res:
            fp.write(el[0])


if __name__ == "__main__":
    main("numbers-large.txt")
