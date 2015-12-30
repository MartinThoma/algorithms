## Get the data

If you're only interested in the data, have a look at
[`MartinThoma/pypi-dependencies`](https://github.com/MartinThoma/pypi-dependencies)


## Install and execute

If you want to use these scripts, please

1. Install a MySQL server
2. Add a database `pypi` to the MySQL server
3. Add the MySQL database scheme from `database_schema.sql`
4. Install Python requirements via `sudo pip install -r requirements.txt`
   or `sudo pip3 install -r requirements.txt`
5. Copy `secret.template.json` to `secret.json` in the same folder and adjust
   the values.

To fill the database, run

6. `./build_datastructure.py` (takes several hours)
7. `./add_system_packages.py` (takes a few seconds)

If you have at least 50GB of disc space free, you can run

8. `./build_dependency_db.py` (takes many many hours - probably even several days)

You might want to examine the files:

* `not-found.csv`: Imports which were not found on PyPI.
   (try `sort not-found.csv | uniq > not-found-sorted.csv`)
* `todo-unknown-pkg-extension.csv`: Package extensions which were not analyzed
  AND not seen before.

## See also
https://pypi.python.org/pypi/bandersnatch


## Empty Packages
* exodata

## Errors

* 2015-12-06 22:43:30,623 ERROR '2' gave HTTP Error 404: Not Found
* 2015-12-06 22:43:37,068 ERROR 'abu.rpc' gave HTTP Error 404: Not Found
* 2015-12-06 22:43:37,553 ERROR 'about-pandoc' gave HTTP Error 404: Not Found
* 2015-12-06 22:43:37,583 ERROR 'about-numtest' gave HTTP Error 404: Not Found
* 2015-12-06 22:43:39,308 ERROR 'acid' gave HTTP Error 404: Not Found
* 2015-12-06 22:44:12,492 ERROR 'aescalante-nester' gave HTTP Error 404: Not Found
* 2015-12-06 22:45:01,173 ERROR 'amoeba' gave HTTP Error 404: Not Found
* 2015-12-06 22:45:03,717 ERROR 'amqp1.0' gave HTTP Error 404: Not Found
* 2015-12-06 22:45:06,080 ERROR 'anansi' gave HTTP Error 404: Not Found
* 2015-12-06 22:45:28,273 ERROR 'antlr4-python' gave HTTP Error 404: Not Found
...