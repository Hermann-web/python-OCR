import os,re
import string 
from pdf_to_img import pdf_to_img #import a function to convert into image 
from img_to_txt import img_to_txt
import img2pdf #pip install img2pdf
#------------------------------------------------------------------------------------

'''
for fc in Factures:
    fc['fourniseur']: fournisseur  
    fc['num_facture']: num_facture 
    fc['Pages']:zip(list_img_to_merge,list_textePage,list_index)
'''
def pdf_to_txt(pdf_abspath):
    return {[
    {   'fourniseur': ':fournisseu',
        'num_facture': ':num_fact',
        'Pages':{(':img_pt',':textpage',':index')}
    }]}
    print('Step1: get images')
    list_img_path = pdf_to_img(pdf_abspath) #get first image (page1) 
    print('Step2: get texts')
    Factures = get_string(list_img_path)
    return Factures
    

    
def get_string(list_img_path):
    Liste_string=[] #liste des textes_factures
    current_index=0 #index à parti duquel on fait le merge des images
    current_vendor = '' #nom du fournisseur 
    current_invoice_num = ''
    Factures = []

    print('--getting images from path--',end='\n  ')
    for i,img_path in enumerate(list_img_path):
        
        data_img = {}
        print(f'page{i}',end = ' ')
        
        print('--converting image to texte')
        textePage = img_to_txt(img_path)
        #store_txt
        with open(img_path+'.txt','w') as f:
            f.write(textePage)
            data_img['textpage']=textePage
        
        #founisseur
        print('--getting vendor name--')
        fournisseur = get_vendor_name(textePage)
        data_img['fournisseur']=fournisseur

        #num facture
        if not fournisseur: 
            print('vendor not found')
            num_facture=''
        else:
            print('vendor found:',fournisseur)
            print('get invoice number')
            num_facture = get_num_facture(textePage,fournisseur)
        data_img['num_facture']=num_facture
        
        Factures.append({})
        last_facture = Factures[-1]
        last_facture['fourniseur'] = fournisseur
        last_facture['num_facture'] = num_facture
        last_facture['pages'] = []
        last_facture['pages'].append([img_path,textePage,i])


    for i,fc in enumerate(Factures):
        fournisseur = fc['fourniseur']
        num_facture = fc['num_facture']
        pages = fc['pages']
        list_img_to_merge,list_textePage,list_index = list(zip(*pages))


        #merge text
        sep = 5*('\n'+20*'######')
        Liste_string.append(sep.join(list_textePage))

        #merge img
        pdf_path = merge_img(list_img_to_merge=list_img_to_merge,vendor=fournisseur,invoice_num=num_facture,list_idx=list_index)
        #store pdf file path
        Factures[i]['pdf_file_path'] = pdf_path

    print('\n')
    return Factures

def merge_img(list_img_to_merge,vendor,invoice_num,list_idx):
    print(f'--identification of a invoice from pages:{list_idx} \n    vendor_name={vendor}   invoice_number={invoice_num}---')
    print('merging')
    pdf_path = merge_and_store(list_img_to_merge,vendor,invoice_num)
    return pdf_path

def merge_and_store(list_img_to_merge,fournisseur,numero_de_facture):
    print('--merging docs---')
    #print()
    output_path = f'{fournisseur}&&{numero_de_facture}.pdf'
    with open(output_path,"wb") as f:
        f.write(img2pdf.convert([remove_alpha_from_image(path) for path in list_img_to_merge]))
    return output_path



PUNCTUATION = string.punctuation
TEMPLATE_NUM_FACTURE_STR = 'Template'
DIGIT_STR = 'Number'
CHAR_STR = 'Character' #ex f,g,h
CHAR_UPPER_STR = 'UpperCharacter'
CHAR_LOWER_STR = 'LowerCharacter'
NOMS_POSSIBLES = 'NOMS_POSSIBLES'
DICT_REGEX = {
        DIGIT_STR: '\d',
        CHAR_STR: '[a-zA-Z]',
        CHAR_UPPER_STR: '[A-Z]',
        CHAR_LOWER_STR: '[a-z]'
        }

#Specials chars
'''
from string import punctuation
LIST_SPECIAL_CHARS = list(punctuation)
LIST_SPECIAL_CHARS.remove('_')
'''
JSON = {'SEFI':{
                TEMPLATE_NUM_FACTURE_STR :[(DIGIT_STR,6)],
                NOMS_POSSIBLES : ['SEFI'],
                },
        'PPG':{
                TEMPLATE_NUM_FACTURE_STR :[(DIGIT_STR,10)],
                NOMS_POSSIBLES : ['PPG','PPG Coatings'],
                }
        }

#cette fonction récupère un texte et cherche le numero de facture. Il retourne False au cas échéant
def get_num_facture(textePage,fournisseur):
    print('--searching invoice_number--')
    STOP = ' '
    textePage = re.sub(r'\s+',STOP, textePage) #je remplate tous les whitespace par ' '
    template = JSON[fournisseur][TEMPLATE_NUM_FACTURE_STR] #template ex: [(DIGIT_STR,5),] 
    liste_possibilites = ismatch(textePage,template)
    print(liste_possibilites)
    return liste_possibilites[0] if liste_possibilites else False

def ismatch(sequence,template):
    print('--searching for a match ..')
    regex=''
    for tuple in template:
        expression,occurence = tuple[0], tuple[1]
        if expression in DICT_REGEX:
            print(expression, 'found in DICT_REGEX')
            regex += DICT_REGEX[expression]
        elif expression in PUNCTUATION:
            print(expression, 'found in PUNCTUATION')
            regex += "\\"+expression
        else:
            print(expression, 'not found in DICT_REGEX nor PUNCTUATION')
            regex += "("+expression+")"

        regex += '{'+str(occurence)+'}'
    regex = "\\" + "b" + regex + "\\" +'b'
    print('regex: ',[regex])
    
    return re.findall(regex,sequence) or []
        
#check in a vendor_name is found, otherwise false
def get_vendor_name(result):
    print('--searching vendor name--')
    for vendor in JSON:
        for vendor_name in JSON[vendor][NOMS_POSSIBLES]:
            if foundInpage(vendor_name,result):
                print('--found--')
                return vendor
    print('--not found--')
    return False     

#check in a vendor is found in a page
def foundInpage(vendor,textpage):
    print(f'{vendor}')
    found = vendor.upper() in textpage.upper()
    if found:
        idx = textpage.upper().index(vendor.upper())
        print('here:',textpage[idx:min(idx+50,len(textpage)-1)])
        print(textpage.upper().index(vendor.upper()))
        return True 
    else:
        return False

#pdf_abspath = "data/pdf/FactureSNM/document-page1.pdf"
#pdf_to_txt(pdf_abspath)

from PIL import Image as PILImage
from hashlib import md5
TMP_DIR = 'data/tmp/'
def remove_alpha_from_image(image_path):
    im = PILImage.open(image_path)
    im.load()
    try:
        background = PILImage.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3])  # 3 is the alpha channel
        im = background
    except IndexError:  # img is not RGBA
        pass

    name_hash_md5 = md5(bytes(image_path, encoding="utf-8"))  # noqa: S303
    name = name_hash_md5.hexdigest()
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    path = f"{TMP_DIR}{name}.pdf"
    im.save(path, "PNG", resolution=100.0)
    return path
#imagemagick convert -density 192 document-page1.pdf page1.png
#imagemagick convrt -density 500 document-page1.pdf -resize 25% page1.png
#convert input.png -background white -alpha remove -alpha off output.png

if __name__ == '__main__':
    img_path = "data/pdf/Echantillon Facture SNM _imgs_3/page_0.jpeg"
    #img_path ="data\\pdf\\FactureSNM\document-page0_imgs_900\page_0.jpeg"
    img_path = "data\pdf\FactureSNM\document-page0_imgs_900\page_0.jpeg"
    img_path = "data/pdf/FactureSNM/document-page1_imgs_900/page_0.jpeg"
    #img_path = "data/pdf/FactureSNM/document-page1_imgs_900/index.png"
    img_path = "data/pdf/FactureSNM/page1.png"
    
    img_path = remove_alpha_from_image(img_path)
    list_img_path = [img_path]
    print(get_string(list_img_path))
