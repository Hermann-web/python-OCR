import os
from pdf_to_img import pdf_to_img #import a function to convert into image 
from img_to_txt import img_to_txt
import img2pdf #pip install img2pdf
#------------------------------------------------------------------------------------

def pdf_to_txt(pdf_abspath):
    list_img_path = pdf_to_img(pdf_abspath) #get first image (page1) 
    liste_txt = get_string(list_img_path)
    return liste_txt
    
    
    
def get_string(list_img_path):
    Liste_string=[] #liste des textes_factures
    current_index=0 #index à parti duquel on fait le merge des images
    current_vendor = '' #nom du fournisseur 
    current_invoice_num = ''
    print('--getting images from path--',end='\n  ')
    for i,img_path in enumerate(list_img_path):
        print(f'page{i}',end = ' ')
        
        textePage = img_to_txt(img_path)
        fournisseur = get_vendor_name(textePage)
        
        #check if there is another invoice
        if fournisseur and (fournisseur!=current_vendor):
            current_vendor = fournisseur
            current_invoice_num = get_num_facture(textePage,current_vendor)
            Liste_string.append(textePage)
        else:
            Liste_string[-1]+=textePage
            list_img_to_merge  = list_img_path[current_index:i];current_index = i
            merge_and_store(list_img_to_merge,fournisseur,current_invoice_num)
            
    print('\n')
    return Liste_string

def merge_and_store(list_img_to_merge,fournisseur,numero_de_facture):
    output_path = f'{fournisseur}&&{numero_de_facture}.pdf'
    with open(output_path,"wb") as f:
        f.write(img2pdf.convert(list_img_to_merge))
    return output_path

TEMPLATE_NUM_FACTURE_STR = 'Template'
DIGIT_STR = 'Number'
CHAR_STR = 'Character' #ex f,g,h
CHAR_UPPER_STR = 'UpperCharacter'
CHAR_LOWER_STR = 'LowerCharacter'

DICT_REGEX = {
        DIGIT_STR: '\d',
        CHAR_STR: '[a-zA-Z]',
        CHAR_UPPER_STR: '[a-zA-Z]',
        CHAR_LOWER_STR: '[a-zA-Z]'
        }

JSON = {'SEFI':{
                TEMPLATE_NUM_FACTURE_STR :(DIGIT_STR,6),
                NOMS_POSSIBLES : ['SEFI','SEF'],
                }
        }

 


#cette fonction récupère un texte et cherche le numero de facture. Il retourne False au cas échéant
def get_num_facture(textePage,fournisseur):
    STOP = ' '
    textePage = re.sub(r'\s+',STOP, txt)
    template = JSON[fournisseur][TEMPLATE_STR] #template ex: [(DIGIT_STR,5),]  
    for sequence in x.split(STOP):
        if ismatch(sequence,template): return sequence
    return False

def ismatch(sequence,template):
    regex = ''
    for tuple in template:
        expression,occurence = tuple[0], tuple[1]
        if expression in DICT_REGEX:
            regex += DICT_REGEX[expression]
        else:
            regex += expression
        regex += f'{{occurence}}'
    return re.match(regex,sequence)
    
        
#check in a vendor_name is found, otherwise false
def get_vendor_name(result):
    for vendor in JSON:
        for vendor_name in Dict[vendor]:
            if foundInpage(vendor_name,result):
                return vendor
    return False     
    
    
#check in a vendor is found in a page
def foundInpage(vendor,textpage):
    return vendor.upper() in textpage.upper()






