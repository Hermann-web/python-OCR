# python-OCR

In accounting, working with thousands of vendors is quite challenging when it comes to search invoices by invoice number between scanned documents.

Text invoices contain variety of information such as product names, VAT, product prices, vendor or customer names, tax information, the date of the transaction etc. The process of reading text from images is called Object Character Recognition since characters in images are essentially treated as objects.

In this repository, i have gone trough some ways de convert pdf to images using python. The, we can read text from these images. A little further content extraction is not provided here


#Prerequistes
- Tesseract: https://github.com/tesseract-ocr/tesseract
- ImageMagick: https://github.com/ImageMagick/ImageMagick 
- ghostscript: https://www.ghostscript.com/download/gsdnld.html



Bibliographie
- https://hypi.io/2019/10/29/reading-text-from-invoice-images-with-python/
- invoice2data, a python library: https://medium.com/version-1/my-experience-extracting-invoice-data-using-invoice2data-in-python-1c6450fa001f
- https://datascience.stackexchange.com/questions/33231/using-python-and-machine-learning-to-extract-information-from-an-invoice-inital
- using pdf2image ans easyocr: https://www.youtube.com/watch?v=bcmEMcEzV9M
- some insight of my solution: https://datascience.stackexchange.com/questions/33231/using-python-and-machine-learning-to-extract-information-from-an-invoice-inital
- crreate rectangles in the pdf file using ocrmypdf: https://www.youtube.com/watch?app=desktop&v=glJi3LBgn9U
- a similar project in C#: https://github.com/robela/OCR-Invoice
- veryfi: an excellent API to get informations from an invoice or receipt: https://www.linkedin.com/pulse/extract-data-from-receipt-invoice-5-lines-ofcode-dmitry-birulia/?articleId=6676262454793764864
- Others: https://hypi.io/2019/10/29/reading-text-from-invoice-images-with-python/; 
