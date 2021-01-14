import zipfile

zp = zipfile.ZipFile("example.zip")

size = sum([zinfo.file_size for zinfo in zp.filelist])
zip_kb = float(size) / 1000  # kB
