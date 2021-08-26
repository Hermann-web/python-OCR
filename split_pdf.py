from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("data/pdf/Echantillon Facture SNM .pdf", "rb"))

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("data/pdf/document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)