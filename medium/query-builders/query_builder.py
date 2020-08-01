# Core Library modules
from typing import List

# Third party modules
import pymysql.cursors
from pypika import Query, Table

# First party modules
from raw_sql import db_connection


@db_connection
def get_titles_by_author(con, author_id: int) -> List[str]:
    books = Table()
    q = Query.from_(books).select("*").where(books.author_id == author_id)
    cur = con.cursor(pymysql.cursors.DictCursor)
    query = q.get_sql(quote_char=None)
    cur.execute(query)
    titles = [row["title"] for row in cur.fetchall()]
    return titles


if __name__ == "__main__":
    print(get_titles_by_author(1))
