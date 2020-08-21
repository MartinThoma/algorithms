import pprint

import click
import fitz  # pip install pymupdf


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def entrypoint(filepath):
    pp = pprint.PrettyPrinter(indent=4)
    with fitz.open(filepath) as doc:
        pp.pprint(doc.metadata)
        print(f"Scanned pages: {get_scanned_pages_percentage(filepath) * 100:0.1f}%")


class NoTextPagesException(RuntimeError):
    pass


def get_scanned_pages_percentage(filepath: str) -> float:
    """
    Return the percentage of pages with text which were scanned.

    Note that this could raise a NoTextPagesException.
    """
    total_pages = 0
    total_scanned_pages = 0
    with fitz.open(filepath) as doc:
        for page in doc:
            text = page.getText().strip()
            if len(text) == 0:
                # Ignore "empty" pages
                continue
            total_pages += 1
            pix1 = page.getPixmap(alpha=False)  # render page to an image
            pix1.writePNG(f"page-{page.number}.png")  # store image as a PNG
            remove_all_text(doc, page)
            pix2 = page.getPixmap(alpha=False)
            pix2.writePNG(f"page-{page.number}-no-text.png")
            img1 = pix1.getImageData("png")
            img2 = pix2.getImageData("png")
            if img1 == img2:
                print(f"{page.number} was scanned or has no text")
                if len(text) > 0:
                    print(f"\tHas text of length {len(text):,} characters")
                    total_scanned_pages += 1
            else:
                print(f"{page.number} was NOT scanned")
    if total_pages == 0:
        raise NoTextPagesException
    return total_scanned_pages / total_pages


def remove_all_text(doc, page):
    page.cleanContents()  # syntax cleaning of page appearance commands

    # xref of the cleaned command source (bytes object)
    xref = page.getContents()[0]

    cont = doc.xrefStream(xref)  # read it
    ba_cont = bytearray(cont)  # a modifyable version
    pos = 0
    changed = False  # switch indicates changes
    while pos < len(cont) - 1:
        pos = ba_cont.find(b"BT\n", pos)  # begin text object
        if pos < 0:
            break  # not (more) found
        pos2 = ba_cont.find(b"ET\n", pos)  # end text object
        if pos2 <= pos:
            break  # major error in PDF page definition!
        ba_cont[pos : pos2 + 2] = b""  # remove text object
        changed = True
    if changed:  # we have indeed removed some text
        doc.updateStream(xref, ba_cont)  # write back command stream w/o text


if __name__ == "__main__":
    entrypoint()
