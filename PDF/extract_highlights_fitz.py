# Based on https://stackoverflow.com/a/62859169/562769

from typing import List

import fitz  # install with 'pip install pymupdf'


def _parse_highlight(annot: fitz.Annot, wordlist: List) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = ["" for i in range(quad_count)]
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect
        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences[i] = " ".join(w[4] for w in words)
    sentence = " ".join(sentences)
    return sentence


def handle_page(page):
    wordlist = page.getText("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights


def main(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights


if __name__ == "__main__":
    print(main("PDF-export-example-with-notes.pdf"))
