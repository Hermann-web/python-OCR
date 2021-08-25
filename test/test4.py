#https://xiaofeima1990.github.io/2016/12/19/extract-text-from-sanned-pdf/

from wand.image import Image #import wand #installer ImageMagick
from PIL import Image as PI #import ?
import pyocr #import pyocr mais il marche pas sans 
import pyocr.builders
import io



def way(path):

    print('--getting tools--')
    
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0] # 0 is eng

    req_image = []
    final_text = []
    
    print('--converting pdf--')

    image_pdf = Image(filename=path, resolution=600)
    image_jpeg = image_pdf.convert('jpeg')
    
    
    print('--getting pages--')

    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))
    print('--getting text--')
    for i,img in enumerate(req_image): 
        print(f'page{i}')
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
    return final_text

path = "data\\pdf\\Echantillon Facture SNM .pdf"
texte  = way(path)
import os
fname = os.path.basename(path)  #os.path.splitext(path)[0].split('\\')[-1]
with open(f'file_{fname}.txt','w') as f:
    f.write('\n\n\n-----------------------------------------------------------------------------------------------------------\n\n\n'.join(texte))
    print(texte[:min(1000,len(texte)-1)])
    