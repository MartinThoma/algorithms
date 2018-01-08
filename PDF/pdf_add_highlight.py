from PyPDF2 import PdfFileWriter, PdfFileReader

from PyPDF2Highlight import createHighlight, addHighlightToPage

pdfInput = PdfFileReader(open("early-stopping-1703.09580.pdf", "rb"))
pdfOutput = PdfFileWriter()

page1 = pdfInput.getPage(0)
number_of_pages = pdfInput.getNumPages()
page_content = page1.extractText()
import textract
text = textract.process("early-stopping-1703.09580.pdf")
print page_content.encode('utf-8')

highlight = createHighlight(488.725021, 202.392357, 523.153376, 211.298922, {
    "author": "",
    "contents": "Bla-bla-bla"
})

addHighlightToPage(highlight, page1, pdfOutput)

pdfOutput.addPage(page1)

outputStream = open("output.pdf", "wb")
pdfOutput.write(outputStream)