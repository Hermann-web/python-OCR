from pdf2image import convert_from_path
import os
images = convert_from_path("data/pdf/EDP-etudiants.pdf", 500,poppler_path=r"lib/poppler-0.68.0_x86/poppler-0.68.0/bin")
for i, image in enumerate(images):
    dir = "data/pdf"
    fname = os.path.join(dir,'image_EDP'+str(i)+'.png')
    image.save(fname, "PNG")
    print('1 saved')