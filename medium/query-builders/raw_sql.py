import os
from typing import List

import pymysql.cursors


def db_connection(f):
    """
    Supply the decorated function with a database connection.

    Commit/rollback and close the connection after the function call.
    """

    def with_connection_(*args, **kwargs):
        con = pymysql.connect(
            host="localhost",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            db="books",
        )
        try:
            rv = f(con, *args, **kwargs)
        except Exception:
            con.rollback()
            raise
        else:
            con.commit()
        finally:
            con.close()

        return rv

    return with_connection_


@db_connection
def get_titles_by_author(con, author_id: int) -> List[str]:
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT * FROM books WHERE author_id = %s", author_id)
    titles = [row["title"] for row in cur.fetchall()]
    return titles


if __name__ == "__main__":
    print(get_titles_by_author(1))
