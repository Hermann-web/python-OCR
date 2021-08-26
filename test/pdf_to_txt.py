import os 

####avec pytesseract et PIL.image
# Great !!! Il transforme en texte corectement les plus compliqués

import cv2 ##pip install opencv-python
import numpy as np
import pytesseract #pip install pytesseract #installer tesseract et mettre le lien vers le exe dans le code 

#  Set the tesseract path in the script before calling image_to_string
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def get_string_way1(list_img_path):
    from PIL import Image as PILImage
    print('--getting string from imagePages--',end='\n  ')
    Liste_string=[]
    for i,img_path in enumerate(list_img_path):
        print(f'page{i}',end = ' ')
        # Recognize text with tesseract for python
        result = pytesseract.image_to_string(PILImage.open(img_path))
        Liste_string.append(result)
    print('\n')
    return Liste_string

#Il veut enlever du bruit: Il fait juste plus bizarre non ??
#  Set the tesseract path in the script before calling image_to_string
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def get_string_way2(list_img_path):
    from PIL import Image as PILImage
    print('--getting string from imagePages--',end='\n  ')
    Liste_string=[]
    for i,img_path in enumerate(list_img_path):
        print(f'page{i}',end = ' ')
        # Read image with opencv
        img = cv2.imread(img_path)
        
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

        # Recognize text with tesseract for python
        result = pytesseract.image_to_string(PILImage.open(img_path))
        Liste_string.append(result)
    print('\n')
    return Liste_string



##########avec pytesseract et pyocr  #il fait bizarre sur le pdf1
#https://xiaofeima1990.github.io/2016/12/19/extract-text-from-sanned-pdf/

from wand.image import Image #import wand #installer ImageMagick
from PIL import Image as PI #import ?
import pyocr #import pyocr mais il marche pas sans des way liées à tesseract
import pyocr.builders
import io

def get_string_way3(list_img_path):

    print('--getting tools--')
    
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0] # 0 is eng

    req_image = []
    final_list_of_text = []
    print('--getting images from path--',end='\n  ')
    for i,img_path in enumerate(list_img_path):
        print(f'page{i}',end = ' ')
        img_page = Image(filename=img_path)
        req_image.append(img_page.make_blob('jpeg'))
    print('\n')
    print('--getting text--',end='\n  ')
    for i,img in enumerate(req_image): 
        print(f'page{i}',end = ' ')
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_list_of_text.append(txt)
    print('\n')
    return final_list_of_text
    
    

def pdf_to_txt(pdf_abspath):
    from pdf_to_img import pdf_to_img #import a function to convert into image 
    list_img_path = pdf_to_img(pdf_abspath) #get first image (page1) 
    liste_txt = get_string_way1(list_img_path))
    return list_img_path

if __name__ == '__main__':
    pdf = "data/pdf/pdf1.pdf"
    #pdf = "data/pdf/Echantillon Facture SNM .pdf"

    from pdf_to_img import pdf_to_img #import a function to convert into image 
    pdf = os.path.abspath(pdf) #get abs path 
    list_img_path = pdf_to_img(pdf) #get first image (page1) 

    sep = '\n\n'.join(5*[100*'-'])
    print (sep.join(get_string_way1(list_img_path)))


