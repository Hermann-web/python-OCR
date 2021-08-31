
import os

#not working!!!!! because of poppler 
##https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
def way1(filepath):
    from pdf2image import convert_from_path #Installer le poppler, mettre le bin en path, et dans le code ci
    print('--converting pdf--')
    images = convert_from_path(filepath, 500,poppler_path=r"lib/poppler-0.68.0_x86/poppler-0.68.0/bin")
    for i, image in enumerate(images):
        #dir = os.path.abspath( os.path.join(filepath,'..'))
        #filename = os.path.basename(filepath).split('.')[:-1]
        image_folder = get_image_folder(filepath,add='1')
        
        filepath = os.path.join(image_folder, f'page_{i}.png')
        image.save(filepath, "PNG")
        print('1 saved')

#working
#mauvaise résolution sur les images bizares
def way2(filepath):
    from wand.image import Image as wandImage #need to install IMageMagick (to convert pdf to img) and ghostscript (to read pfd)
    Liste_path = []
    print('--converting pdf--')
    with wandImage(filename=filepath) as img:
        image_folder = get_image_folder(filepath,add='2')
        print('pages = ', len(img.sequence))
        with img.convert('png') as converted:
            imgpath = os.path.join(image_folder, 'pages.png')
            converted.save(filename=imgpath)
            Liste_path.append(imgpath)
    return Liste_path
#imgpath = '..../pages.png' --> Liste_path = ['..../pages-0.png','..../pages-1.png','..../pages-2.png','..../pages-3.png','..../pages-4.png','..../pages-5.png',.....] au lieu de ['..../pages.png']. du coup, le return n'est pas bon 

#working #Excellent!!! Passer la résolution à 900 fait que toutes les méthodes de img_to_txt marchent
#il est mieux que way 2 car on peut augmenter la resolution et preciser les nom des pages as images
def way3(filepath):
    from wand.image import Image as wandImage #need to install IMageMagick (to convert pdf to img) and ghostscript (to read pfd)
    req_image = []   
    Liste_path = []
    resolution = 900
    image_folder = get_image_folder(filepath,add=str(resolution))
    print('--converting pdf--')
    image_pdf = wandImage(filename=filepath, resolution=resolution)
    image_jpeg = image_pdf.convert('jpeg')
    print('--getting pages--',end='\n ')
    for i,img in enumerate(image_jpeg.sequence):
        print(f'page{i}',end = ' ')
        img_page = wandImage(image=img)
        imgpath = os.path.join(image_folder, f'page_{i}.jpeg')
        img_page.save(filename=imgpath)
        Liste_path.append(imgpath)
    print('\n')
    return Liste_path

    
        
#codes
def get_image_folder(pdf_path,add=''):
    image_folder = '.'.join(pdf_path.split('.')[:-1])+'_imgs_'
    if add: image_folder = image_folder+add
    if not os.path.exists(image_folder): os.makedirs(image_folder) 
    return image_folder


def pdf_to_img(filepath):
    return way3(filepath)

if __name__ == '__main__':
    #filename = "data/pdf/EDP-etudiants.pdf"
    filename = "data/pdf/facture1.pdf"
    way2(filename)