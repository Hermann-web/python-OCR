import os
from pdf_to_txt import pdf_to_txt

def get_dir(path):
	split_url = path.split('%2f')[1:]
	split_url = [elt.replace('%20',' ') for elt in split_url]
	split_url[-1] = split_url[-1].split('&')[0]
	url_part1 = "//inshare.collab.group.safran@SSL/"
	url_part2 = "/".join(split_url)
	return url_part1 +url_part2


def get_files_from_folder(folder_url):
    dir = get_dir(folder_url)
    liste_files_path = os.listdir(dir)
    liste_files_abs_path = [os.path.join(dir,elt) for elt in liste_files_path]
    return liste_files_abs_path

def process(liste_folders):
    for url in liste_folders:
        liste_pdf_files_path = get_files_from_folder(folder_url)
        for pdf_file_path in liste_pdf_files_path:
            liste_text_pages = pdf_to_txt(pdf_file_path)


def test():
    URL = "https://inshare.collab.group.safran/bao/CSPFin/_layouts/15/start.aspx#/Processus%20paiement%20et%20trsorerie/Forms/AllItems.aspx?RootFolder=%2fbao%2fCSPFin%2fProcessus%20paiement%20et%20trsorerie%2fSAFRAN%20MAROC%2fTest%20factures&FolderCTID=0x01200005E92C016C86064F9DE0ACDC48CEC253"

    import os 
    dir = get_dir(URL)
    print(os.listdir(dir))
