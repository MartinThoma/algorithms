import uuid


def create_uuids(filename, n=10 ** 7):
    with open(filename, "w") as f:
        for _ in range(n):
            f.write(str(uuid.uuid4()) + "\n")


create_uuids("uuids.csv", n=10 ** 6)
