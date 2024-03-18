import os
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


def partial_shuffle(mapping: list[tuple[str, str]]) -> dict[str, str]:
    original = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .:!?,"
    )
    shuffled = dict(mapping)

    # Add remaining characters not specified in the mapping
    remaining_chars = [char for char in original if char not in shuffled.keys()]
    for char in remaining_chars:
        shuffled[char] = char

    return shuffled


def manipulate_font(font_name: str, mapping: tuple[str, str]) -> tuple[str, str]:
    # Load the original font
    location = find_font(name=font_name)
    font = TTFont(location)

    # Iterate through each char in the original and apply mapping
    shuffle_mapping = partial_shuffle([mapping])
    for char, rotated_char in shuffle_mapping.items():
        try:
            o_glyph = font["cmap"].getcmap(3, 1).cmap[ord(char)]
            r_glyph = font["cmap"].getcmap(3, 1).cmap[ord(rotated_char)]
            font["cmap"].getcmap(3, 1).cmap[ord(char)] = r_glyph
            font["cmap"].getcmap(3, 1).cmap[ord(rotated_char)] = o_glyph
        except KeyError:
            print(f"Glyph data not found for character '{char}'")

    # Change font name
    new_name = str(uuid.uuid4())
    for record in font["name"].names:
        if record.nameID == 1:  # Font Family name
            record.string = new_name.encode("utf-16-be")

    # Save the modified font to a new font file
    out = f"rotated_font-{new_name}.ttf"
    font.save(out)
    return out, new_name


def generate_pdf(shown_message: str, hidden_message: str) -> None:
    # Pad the shorter message with spaces
    max_length = max(len(hidden_message), len(shown_message))
    hidden_message = hidden_message.ljust(max_length)
    shown_message = shown_message.ljust(max_length)

    # Create a PDF instance
    pdf = FPDF()
    pdf.add_page()

    x_position = 10  # Adjust this value as needed
    y_position = 10
    cell_width = 5

    for shown, hidden in zip(shown_message, hidden_message):
        # Add the custom font
        font_path, font_name = manipulate_font("LibrestileExtBold", (shown, hidden))
        pdf.add_font(font_name, "", font_path, uni=True)
        pdf.set_font(font_name, "", 16)

        # Add text using the custom font
        pdf.set_xy(x_position, y_position)  # Set x and y position
        pdf.cell(cell_width, 1, txt=hidden, ln=False, align="L")
        x_position += cell_width
        if x_position > 200:
            x_position = 10
            y_position += cell_width * 2

    # Output the PDF
    pdf_file_path = "2_example.pdf"
    pdf.output(pdf_file_path)


if __name__ == "__main__":
    generate_pdf(
        shown_message="This text is written using the custom font",
        hidden_message="Never gonna give you up, never gonna let you down",
    )
