import os
import random
import uuid

from fontTools.ttLib import TTFont  # pip install fonttools
from fpdf import FPDF  # pip install fpdf2


def find_font(name: str = "Helvetica") -> str:
    common_locations = [
        f"{name}.ttf",
        f"/Library/Fonts/{name}.ttf",  # macOS
        f"/usr/share/fonts/truetype/msttcorefonts/{name}.ttf",  # Linux
        f"/usr/local/share/fonts/{name}.ttf",  # Linux
        f"/usr/share/fonts/{name}.ttf",  # Linux
        f"C:\\Windows\\Fonts\\{name}.ttf",  # Windows
    ]

    for location in common_locations:
        if os.path.exists(location):
            return location
    raise RuntimeError(f"Font '{name}' not found")


def manipulate_font(font_name: str) -> str:
    # Load the original font
    location = find_font(name=font_name)
    font = TTFont(location)

    # Garble
    original = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    rot = list(original)
    random.shuffle(rot)
    shuffled = "".join(rot)
    shuffle_mapping = dict(zip(original, shuffled))

    # Iterate through each glyph in the original font and apply mapping
    for char, rotated_char in shuffle_mapping.items():
        try:
            o_glyph = font["cmap"].getcmap(3, 1).cmap[ord(char)]
            r_glyph = font["cmap"].getcmap(3, 1).cmap[ord(rotated_char)]
            font["cmap"].getcmap(3, 1).cmap[ord(char)] = r_glyph
            font["cmap"].getcmap(3, 1).cmap[ord(rotated_char)] = o_glyph
        except KeyError:
            print(f"Glyph data not found for character '{char}'")

    # Change font name
    for record in font["name"].names:
        if record.nameID == 1:  # Font Family name
            record.string = "RotatedFont".encode("utf-16-be")

    # Save the modified font to a new font file
    out = f"rotated_font-{uuid.uuid4()}.ttf"
    font.save(out)
    return out


def generate_pdf(text: str, font_path: str) -> None:
    # Create a PDF instance
    pdf = FPDF()
    pdf.add_page()

    # Add the custom font
    pdf.add_font("RotatedFont", "", font_path, uni=True)
    pdf.set_font("RotatedFont", "", 16)

    # Add text using the custom font
    pdf.cell(
        200,
        10,
        txt="This text is written using the custom font!",
        ln=True,
        align="C",
    )

    # Output the PDF
    pdf_file_path = "output.pdf"
    pdf.output(pdf_file_path)


if __name__ == "__main__":
    font_path = manipulate_font("LibrestileExtBold")
    generate_pdf(
        text="This text is written using the custom font!",
        font_path=font_path,
    )
