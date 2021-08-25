from pdf2image import convert_from_path #Installer le poppler, mettre le bin en path, et dans le code ci
import os

def way1(filename):
    images = convert_from_path(filename, 500,poppler_path=r"lib/poppler-0.68.0_x86/poppler-0.68.0/bin")
    for i, image in enumerate(images):
        dir = "data/pdf"
        fname = os.path.join(dir,'image_EDP'+str(i)+'.png')
        image.save(fname, "PNG")
        print('1 saved')


def way2(filename):
    from wand.image import Image
    with Image(filename=filename) as img:
        print('pages = ', len(img.sequence))
        with img.convert('png') as converted:
            converted.save(filename='page.png')


filename = "data/pdf/EDP-etudiants.pdf"
way2(filename)