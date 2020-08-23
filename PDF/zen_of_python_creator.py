import codecs

import this
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

WIDTH, HEIGHT = A4

zen_of_python = codecs.encode(this.s, "rot13").split("\n")
canvas = Canvas("zen-of-python.pdf", pagesize=(WIDTH, HEIGHT))
for y, line in enumerate(zen_of_python, start=0):
    canvas.drawString(72, HEIGHT - y * 20 - 50, line)
canvas.setAuthor("Tim Peters")
canvas.setTitle("The Zen of Python")
canvas.setSubject("PEP-20")
canvas.save()

import fitz

with fitz.open("zen-of-python.pdf") as doc:
    print(doc.metadata)
