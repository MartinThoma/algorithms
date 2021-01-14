# Type annotations are pretty awesome:
# https://medium.com/analytics-vidhya/type-annotations-in-python-3-8-3b401384403d
from typing import Dict

import fitz  # pip install pymupdf


def get_bookmarks(filepath: str) -> Dict[int, str]:
    # WARNING! One page can have multiple bookmarks!
    bookmarks = {}
    with fitz.open(filepath) as doc:
        toc = doc.getToC()  # [[lvl, title, page, …], …]
        for level, title, page in toc:
            bookmarks[page] = title
    return bookmarks


print(get_bookmarks("my.pdf"))
