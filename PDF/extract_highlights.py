#!/usr/bin/env python

from typing import List, Tuple

import poppler


def extract_highlights(filepath: str) -> List[Tuple[int, int, int, int, str]]:
    """
    This is based on code from Marwan Alsabbagh, https://stackoverflow.com/questions/13748242/extracting-pdf-annotations-comments
    see http://socialdatablog.com/extract-pdf-annotations.html
    """
    doc = poppler.document_new_from_file(path, None)
    pages = [doc.get_page(i) for i in range(doc.get_n_pages())]

    for page_no, page in enumerate(pages):
        items = [i.annot.get_contents() for i in page.get_annot_mapping()]
        items = [i for i in items if i]
        for j in items:
            j = j.replace("\r\n", " ")
            j = j.replace("\r\n", " ")
            x = x + "\n\n" + "'{}' (page {})".format(j, page_no + 1)
            if "xk" in j:
                print(j)


if __name__ == "__main__":
    extract_highlights("PDF-export-example-with-notes.pdf")
