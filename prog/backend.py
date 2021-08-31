import os,re
from pdf_to_txt import pdf_to_txt
from datetime import datetime
FORMAT_MONTH = "%Y-%m"



def process(liste_folders):
    print('######init########')
    for url in liste_folders:
        process_folder(get_dir(url))
    print('######end########')
    log = 'ok'
    return log 
    
    
def get_dir(url_dir):
    print('---getting os diractory from url')
    split_url = url_dir.split('%2f')[1:]
    split_url = [elt.replace('%20',' ') for elt in split_url]
    split_url[-1] = split_url[-1].split('&')[0]
    url_part1 = "//inshare.collab.group.safran@SSL/"
    url_part2 = "/".join(split_url)
    return url_part1 +url_part2
    

'''
input: un folder utl 
fonctions:
    - getting files from folder
    - text rendering
    - storing
output: None
'''
def process_folder(folder_url): 
    print('---getting files from folder for text rendering and storing---')
    #on trouve le bon chemin (OS) à partir du url (Sharepoint)
    liste_pdf_files_path = get_files_from_folder(folder_url)
    #on parcoure les groupe_de_factures 
    for pdf_file_path in liste_pdf_files_path:
        #on transforme chaque page du pdf en un texte
        Factures = pdf_to_txt(pdf_file_path)
        Dict_groupe = transform_data(Factures)
        save_values(Dict_groupe)

def get_files_from_folder(folder_url):
    print('---getting pdf files in folder---')
    #folder_url = get_dir(folder_url)
    liste_files_path = os.listdir(folder_url)
    liste_files_abs_path = [os.path.join(folder_url,elt) for elt in liste_files_path]
    return liste_files_abs_path

def transform_data(factures,folder_url,pdf_file_path):
    Dict_pdf_groupe = {}
    Dict_pdf_groupe['date_ajout'] = datetime.now().strftime(FORMAT_MONTH)
    Dict_pdf_groupe['url'] = pdf_file_path
    Dict_pdf_groupe['folder_url'] = folder_url
    Dict_pdf_groupe['invoices'] = [
                {
                    'fourniseur': fc['fourniseur'],
                    'num_facture': fc['num_facture'],
                    'pdf_file_path': fc['pdf_file_path']
                } 
                for fc in Factures
            ]
    return Dict_pdf_groupe
    

def save_values(Dict_groupe_de_factures,path='json.json'):
    print('---saving values---')
    date = Dict_groupe_de_factures['date_ajout']
    Dict = get_dict()
    if date not in Dict:Dict[date]=[]
    Dict[date].append(Dict_groupe_de_factures)
    save_json(Dict,path)
    
def get_dict(path):
  print('------getting old data---')
  try:
    with open(path,'r') as f:
      Dict = json.load(f)
      print('read')
  except:
    with open(path,'w') as f:
      Dict = {}
      print('write')
      json.dump(Dict,f,indent=4)
  return Dict

def save_json(Dict_added,path):
  print('------saving new data---')
  with open(path,'r') as f:
    Dict = json.load(f)
  with open(path,'w') as f:
    Dict.update(Dict_added)
    json.dump(Dict,f,indent=4)

    
def test():
    URL = "https://inshare.collab.group.safran/bao/CSPFin/_layouts/15/start.aspx#/Processus%20paiement%20et%20trsorerie/Forms/AllItems.aspx?RootFolder=%2fbao%2fCSPFin%2fProcessus%20paiement%20et%20trsorerie%2fSAFRAN%20MAROC%2fTest%20factures&FolderCTID=0x01200005E92C016C86064F9DE0ACDC48CEC253"
    
    liste_folders = [URL]
    #process(liste_folders)
    #print('\n\nliste_folders = ',liste_folders,end='\n\n')
    #print(os.listdir(dir))
    
    folder_url = 'data/pdf/onlypdf'
    process_folder(folder_url)

if __name__ == '__main__':
    test()