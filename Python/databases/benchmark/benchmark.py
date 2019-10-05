#!/usr/bin/env python

"""
Test the insertion / selection / deletion speed of a database.

Results
-------
* dict: Inserted 1_000_000 entries in 0.38s (2639859.62 inserts/s). - real398
* memcached: Inserted 10_000 entries in 0.08s (131635.98 inserts/s).
* Sqlite-inmemory: Inserted 1_000_000 entries in 3.85s with ORM-Bulk (259834.14 inserts/s).
* SQLite: Inserted 1_000_000 entries in 5.16s with ORM-Bulk (193930.10 inserts/s).
* Redis: Inserted 100_000 entries in 2.13s (46960.52 inserts/s).
* MySQL (Aria): Inserted 100_000 entries in 21.56s with ORM-Bulk (4638.86 inserts/s).
* Postgres: Inserted 10_000 entries in 2.86s with ORM-Bulk (3494.85 inserts/s).
* MySQL: Inserted 1_000_000 entries in 1987.36s with ORM (503 inserts/s). real    2377,21s

http://www.pytables.org/

Postgres
--------
postgres=# CREATE DATABASE benchmark;
postgres=# \l
postgres=# CREATE USER example_user with encrypted password 'example_password';
postgres=# GRANT all privileges on database benchmark to example_user;
postgres=# \c benchmark;
TRUNCATE "KeyValue";

memcached
---------
$ sudo apt-get install libmemcached-tools
$ memcdump --servers=localhost | wc -l
# Clear all cashes
$ echo 'flush_all' | nc localhost 11211



Redis
-----
$ redis-cli

Delete what is in Redis:
> FLUSHALL
> FLUSHDB

Show what is in Redis:
> KEYS '*'

"""

# core modules
import gc
import json
import random
import time
import uuid

# 3rd party modules
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import click
import numpy as np
import pandas as pd
import sqlalchemy
import redis


Base = declarative_base()

db_dict = {
    "sqlite": "sqlite:///benchmark.db",
    "sqlite-inmemory": "sqlite://",
    "mysql": "mysql+pymysql://root:wert1234@localhost/benchmark",
    "postgres": "postgresql://example_user:example_password@localhost:5432/benchmark",
    "redis": None,
    "memcached": None,
    "dict": None,
}


class KeyValue(Base):
    __tablename__ = "KeyValue"
    key = Column(String(36), primary_key=True)
    value = Column(Text)

    def __repr__(self):
        return f"KeyValue(key='{self.key}', value='{self.value}')"


def run_benchmark(
    SQLALCHEMY_DATABASE_URI, n=1000, batch_size=None, benchmark_type="orm"
):
    if SQLALCHEMY_DATABASE_URI is not None:
        engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

    keys = read_uuids("uuids.csv")
    while len(keys) < n:
        keys.append(str(uuid.uuid4()))
    keys = keys[:n]
    print("finished reading uuids")
    values = [json.dumps([str(uuid.uuid4()) for _ in range(100)]) for i in range(n)]
    print("finished creating values uuids")
    if benchmark_type == "orm":
        benchmark_orm_insert(session, keys, values)
    elif benchmark_type == "orm-bulk":
        truncate_query = """DELETE FROM "KeyValue";"""
        if "mysql" in SQLALCHEMY_DATABASE_URI.lower():
            truncate_query = """DELETE FROM KeyValue;"""
        session.execute(truncate_query)
        benchmark_orm_bulk_insert(session, keys, values, batch_size)
        gc.collect()
        benchmark_orm_bulk_select(session)
        gc.collect()
        select_keys = np.random.choice(keys, 10 ** 6)
        print("Generated selection keys.")
        benchmark_random_selection(session, select_keys)
    elif benchmark_type == "raw":
        benchmark_raw_insert(connection, keys, values)
    elif benchmark_type == "print-inserts":
        print_extended_inserts(keys, values)
    elif benchmark_type == "datafile":
        generate_datafile(keys, values)
    elif benchmark_type == "redis":
        benchmark_redis_insert(keys, values, batch_size=batch_size)
        benchmark_redis_bulk_select()
        select_keys = np.random.choice(keys, 10 ** 6)
        print("Generated selection keys.")
        benchmark_redis_select(select_keys)
    elif benchmark_type == "pickledb":
        benchmark_pickledb_insert(keys, values)
    elif benchmark_type == "memcached":
        benchmark_memcached_insert(keys, values)
        select_keys = np.random.choice(keys, 10 ** 6)
        benchmark_memcached_select(select_keys)
    elif benchmark_type == "dict":
        store = benchmark_dict_insert(keys, values)
        select_keys = np.random.choice(keys, 10 ** 2)
        benchmark_dict_select(store, select_keys)
    else:
        raise NotImplementedError(
            f"benchmark_type={benchmark_type} is not implemented."
        )


def read_uuids(filename):
    with open(filename) as f:
        data = f.read().strip()
    return data.split("\n")


def benchmark_dict_insert(keys, values):
    store = {}
    t0 = time.time()
    for key, value in zip(keys, values):
        store[key] = value
    t1 = time.time()
    print(
        f"dict: Inserted {len(keys)} entries in {t1 - t0:0.2f}s "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s)."
    )
    return store


def benchmark_dict_select(store, keys):
    latencies = []
    for key in keys:
        t0 = time.time()
        key_value = store[key]
        t1 = time.time()
        latencies.append(t1 - t0)
    latencies = np.array(latencies) * 10 ** 6
    print(
        f"Selected {len(keys)} entries in {sum(latencies):0.2f}s "
        f"({len(keys)/sum(latencies):0.2f} selects/s, min={min(latencies):0.0f}μs, "
        f"25%={np.percentile(latencies, 25):0.0f}μs, 50%={np.percentile(latencies, 50):0.0f}μs, "
        f"95%={np.percentile(latencies, 95):0.0f}μs, "
        f"99%={np.percentile(latencies, 99):0.0f}μs, 100%={np.percentile(latencies, 100):0.0f}μs)."
    )


def benchmark_orm_insert(session, keys, values):
    t0 = time.time()
    for key, value in zip(keys, values):
        new_entry = KeyValue(key=key, value=value)
        session.add(new_entry)
    session.commit()
    t1 = time.time()
    print(
        f"Inserted {len(keys)} entries in {t1 - t0:0.2f}s with ORM "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s)."
    )


def benchmark_orm_bulk_insert(session, keys, values, batch_size):
    t0 = time.time()
    batch = []
    for key, value in zip(keys, values):
        batch.append(KeyValue(key=key, value=value))
        if len(batch) == batch_size:
            session.bulk_save_objects(batch)
            batch = []
            session.commit()
    if len(batch) > 0:
        session.bulk_save_objects(batch)
    session.commit()
    t1 = time.time()
    print(
        f"Inserted {len(keys)} entries in {t1 - t0:0.2f}s with ORM-Bulk "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s, batch_size={batch_size})."
    )


def benchmark_orm_bulk_select(session):
    t0 = time.time()
    key_values = session.query(KeyValue).all()
    t1 = time.time()
    print(
        f"Selected {len(key_values)} entries in {t1 - t0:0.2f}s "
        f"({len(key_values)/(t1 - t0):0.2f} selects/s)."
    )


def benchmark_random_selection(session, keys):
    latencies = []
    for key in keys:
        t0 = time.time()
        key_value = session.query(KeyValue).filter(KeyValue.key == key)
        t1 = time.time()
        latencies.append(t1 - t0)
    latencies = np.array(latencies) * 10 ** 6
    print(
        f"Random selected performance for {len(keys)} entries: "
        f"min={min(latencies):0.0f}μs, "
        f"25%={np.percentile(latencies, 25):0.0f}μs, 50%={np.percentile(latencies, 50):0.0f}μs, "
        f"95%={np.percentile(latencies, 95):0.0f}μs, "
        f"99%={np.percentile(latencies, 99):0.0f}μs, 100%={np.percentile(latencies, 100):0.0f}μs)."
    )


def benchmark_redis_insert(keys, values, batch_size):
    """

    Notes
    -----
    Show what is in Redis:
    > KEYS '*'

    Delete what is in Redis:
    > FLUSHDB

    Benchmark Results
    -----------------
    ```
    ## Without the pipeline
    Redis: Inserted 10000 entries in 0.61s (16314.31 inserts/s).

    ## With pipeline
    Redis: Inserted 10000 entries in 0.22s (45966.79 inserts/s).
    ```
    """
    r = redis.Redis(host="localhost")

    t0 = time.time()
    if batch_size is None:
        pipe = r.pipeline()
        for key, value in zip(keys, values):
            pipe.set(key, value)
        pipe.execute()
    else:
        pipe = r.pipeline()
        i = 0
        for key, value in zip(keys, values):
            pipe.set(key, value)
            i += 1
            if i == batch_size:
                i = 0
                pipe.execute()
                pipe = r.pipeline()
        if i > 0:
            pipe.execute()
    t1 = time.time()
    print(
        f"Redis: Inserted {len(keys)} entries in {t1 - t0:0.2f}s "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s)."
    )


def benchmark_redis_select(keys):
    r = redis.Redis(host="localhost")
    latencies = []
    for key in keys:
        t0 = time.time()
        key_value = r.get(key)
        t1 = time.time()
        latencies.append(t1 - t0)
    latencies = np.array(latencies) * 10 ** 6
    print(
        f"Redis: Random get performance for {len(keys)}:"
        f"min={min(latencies):0.0f}us, "
        f"25%={np.percentile(latencies, 25):0.0f}us, 50%={np.percentile(latencies, 50):0.0f}us, "
        f"95%={np.percentile(latencies, 95):0.0f}us, "
        f"99%={np.percentile(latencies, 99):0.0f}us, 100%={np.percentile(latencies, 100):0.0f}us)."
    )


def benchmark_redis_bulk_select():
    r = redis.Redis(host="localhost")
    t0 = time.time()
    keys = r.keys()
    key_values = r.mget(keys)
    t1 = time.time()
    print(
        f"Redis: Selected {len(key_values)} entries in {t1 - t0:0.2f}s "
        f"({len(key_values)/(t1 - t0):0.2f} selects/s)."
    )


def benchmark_memcached_insert(keys, values):
    """
    Benchmark Results
    -----------------
    ```
    ## Without the pipeline
    Redis: Inserted 10000 entries in 0.61s (16314.31 inserts/s).

    ## With pipeline
    Redis: Inserted 10000 entries in 0.22s (45966.79 inserts/s).
    ```
    """
    from pymemcache.client.base import Client

    client = Client(("localhost", 11211))

    t0 = time.time()
    for key, value in zip(keys, values):
        client.set(key, value)
    t1 = time.time()
    print(
        f"memcached: Inserted {len(keys)} entries in {t1 - t0:0.2f}s "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s)."
    )


def benchmark_memcached_select(keys):
    from pymemcache.client.base import Client

    client = Client(("localhost", 11211))

    latencies = []
    for key in keys:
        t0 = time.time()
        key_value = client.get(key)
        t1 = time.time()
        latencies.append(t1 - t0)
    latencies = np.array(latencies) * 10 ** 6
    print(
        f"Memcached: Random get performance for {len(keys)} entries: "
        f"min={min(latencies):0.0f}us, "
        f"25%={np.percentile(latencies, 25):0.0f}us, 50%={np.percentile(latencies, 50):0.0f}us, "
        f"95%={np.percentile(latencies, 95):0.0f}us, "
        f"99%={np.percentile(latencies, 99):0.0f}us, 100%={np.percentile(latencies, 100):0.0f}us)."
    )


def benchmark_pickledb_insert(keys, values):
    import pickledb

    db = pickledb.load("pickle.db", False)
    t0 = time.time()
    for key, value in zip(keys, values):
        db.set(key, value)
    db.dump()
    t1 = time.time()
    print(
        f"PickleDB: Inserted {len(keys)} entries in {t1 - t0:0.2f}s "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s)."
    )


def benchmark_raw_insert(connection, keys, values):
    t0 = time.time()
    statement = text("""INSERT INTO KeyValue(key, value) VALUES(:key, :value)""")
    for key, value in zip(keys, values):
        connection.execute(statement, key=key, value=value)
    t1 = time.time()
    print(
        f"Inserted {len(keys)} entries in {t1 - t0:0.2f}s with raw SQL "
        f"({len(keys)/(t1 - t0):0.2f} inserts/s)."
    )


def print_extended_inserts(keys, values):
    print("INSERT INTO KeyValue (`key`, `value`) VALUES")
    for i, (key, value) in enumerate(zip(keys, values)):
        if i == 0:
            print(f"({json.dumps(key)}, {json.dumps(value)})")
        else:
            print(f", ({json.dumps(key)}, {json.dumps(value)})")
    print(";")


def generate_datafile(keys, values):
    df = pd.DataFrame(data={"key": keys, "value": values})
    df.to_csv("data.csv", index=False, quotechar="'")


@click.command()
@click.option("--db", "db", required=True, type=click.Choice(list(db_dict.keys())))
@click.option("-n", "n", required=True, type=int)
@click.option("--batch-size", "batch_size", required=False, default=None, type=int)
@click.option(
    "--mode",
    "mode",
    required=True,
    type=click.Choice(
        [
            "orm",
            "orm-bulk",
            "raw",
            "print-inserts",
            "datafile",
            "redis",
            "pickledb",
            "memcached",
            "dict",
        ]
    ),
)
def entry_point(db, n, batch_size, mode):
    run_benchmark(db_dict[db], n, batch_size, mode)


if __name__ == "__main__":
    entry_point()
