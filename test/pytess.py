import cv2 ##pip install opencv-python
import numpy as np
import pytesseract #pip install pytesseract
from PIL import Image

# Path of working folder on Disk

#  Set the tesseract path in the script before calling image_to_string
#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\SOS\Documents\Docs\ARRANGER\programmation\python\Projets\PDF_TO_TEXTE\pdfEnv\tesseract\tesseract-ocr-w64-setup-v5.0.0-alpha.20210811.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)
    '''

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite("removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    

    # Write the image after apply opencv to do some ...
    cv2.imwrite(img_path, img)
    '''

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))

    # Remove template file
    #os.remove(temp)

    return result


print ('--- Start recognize text from image ---')
#print (get_string(filename))

print ("------ Done -------")

import os 

pdf = "data/pdf/pdf1.pdf"
image = "data/images/page_pdf1.png"
image = "data/images/image3.jpg"

dir = 'data/images'
filename = 'image3.jpg'
filepath = os.path.join(dir,filename)
filepath = image
print (get_string(filepath))
