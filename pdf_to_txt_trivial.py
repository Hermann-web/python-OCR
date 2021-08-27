filepath = "data/pdf/Echantillon Facture SNM .pdf"
filepath = 'data/pdf/pdf2.pdf' 


#working
import PyPDF2 #pip install ptpdf2
#PyPDF2 cannot read scanned (or image based) files. we'll use an ocr if so
def methode1(filepath):
    Liste_pages=[]
    #open allows you to read the file.
    pdfFileObj = open(filepath,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    for count in range(num_pages):
        text = pdfReader.getPage(count).extractText() #un str
        Liste_pages.append(text)
    return Liste_pages

#was working but now there is a pb 
import textract #pip install textract
#It likely contains a lot of spaces, possibly junk such as '\n,' etc.
def methode2(filepath):
    text = textract.process(filepath, method='tesseract', language='fr')
    return [text]
#better mais il bug sur EDP-Etudiants et la facture scannée


print(methode1(filepath))

'''
methode1,2
    - https://betterprogramming.pub/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f
'''
