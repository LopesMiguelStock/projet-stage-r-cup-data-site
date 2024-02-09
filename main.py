# Importation des bibliothèques nécessaires
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time 
import os
import glob
import uuid
import datetime
import argparse

class Color:
   RED = '\033[91m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   END = '\033[0m'

# Ajout de la fonction pour gérer les arguments de la ligne de commande
def handle_args():
    print("")
    parser = argparse.ArgumentParser(description=Color.GREEN + "Ce script permet de récupérer un point précis d'une page web. " + Color.END + Color.RED + "Attention à selectionner soit l'id ou la classe mais pas les deux en même temps !" + Color.END +
"\n" + Color.BLUE + "Pour modifier la configuration aller dans le fichier config.json ou utiliser les commandes ci-dessous (modifie aussi le fichier config.json)" + Color.END, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--url", metavar='\b', help=Color.CYAN + 'URL à utiliser. Exemple : "https://exemple.com/"' + Color.END)
    parser.add_argument("-t", "--tag", metavar='\b', help=Color.PURPLE + 'Balise HTML à utiliser. Exemple : "div" ou "span", etc' + Color.END)
    parser.add_argument("-c", "--class_name", metavar='\b', help=Color.CYAN + 'Classe CSS à utiliser. Exemple : "maClass"' + Color.END)
    parser.add_argument("-i", "--id", metavar='\b', help=Color.PURPLE + 'ID HTML à utiliser. Exemple : "monID"' + Color.END)
    parser.add_argument("-a", "--all", metavar='\b', help=Color.CYAN + 'Trouver toutes les classes ou ID. Utilisez "yes" ou "no"' + Color.END)
    parser.add_argument("-p", "--proxy", metavar='\b', help=Color.PURPLE + 'Utiliser un proxy. Utilisez "yes" ou "no"' + Color.END)
    parser.add_argument("-x", "--proxy_url", metavar='\b', help=Color.CYAN + 'URL du proxy à utiliser. Exemple : "https://corsproxy.io/?" (optionnel)' + Color.END)
    parser.add_argument("-d", "--directory", metavar='\b', help=Color.PURPLE + 'Dossier à utiliser. Exemple : "monDossier"' + Color.END)
    args = parser.parse_args()
    return args


def update_config(args):
    with open('config.json', 'r+') as file:
        data = json.load(file)
        if args.url: data['url'] = args.url
        if args.tag: data['balise'] = args.tag
        if args.class_name: data['class'] = args.class_name
        if args.id: data['id'] = args.id
        if args.all: data['find_all_class_or_id'] = args.all
        if args.proxy: data['proxy'] = args.proxy
        if args.directory: data['folder'] = args.directory
        if args.proxy_url: data['url_proxy'] = args.proxy_url
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def search():
    # Configuration des options de Chrome
    options = Options()
    options.add_argument('--headless')

    # Configuration de WebDriver
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # Lecture du fichier de configuration
    with open('config.json') as file:
        data = json.load(file)
        url = data['url']
        balise = data['balise']
        class_name = data['class']
        id_name = data['id']
        find_all_class_or_id = data['find_all_class_or_id']
        url_proxy = data['url_proxy']
        proxy = data['proxy']
        folder_name = data['folder']

    # Création du dossier s'il n'existe pas
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Accès à l'URL spécifiée
    driver.get(url_proxy + url if proxy == "yes" else url) 

    # Pause pour permettre le chargement de la page
    time.sleep(5) 

    # Récupération du code source de la page
    resp = driver.page_source 

    # Fermeture du navigateur
    driver.close() 

    # Analyse du code source avec BeautifulSoup
    soup = BeautifulSoup(resp, 'html.parser') 

    # Recherche de l'élément spécifié
    if find_all_class_or_id == 'no':
      output = soup.find(balise, {'class': class_name} if class_name else {'id': id_name})
    else:
      output = soup.find_all(balise, {'class': class_name} if class_name else {'id': id_name})

    # Conversion de 'output' en chaîne
    output_str = str(output)

    # Vérification si 'output' contient "none" ou "[]"
    if "none" == output_str or "[]" == output_str or "None" == output_str:
        print("Output contient 'none' ou '[]'. Aucun fichier n'est créé.")
    else:
        # Création d'un nouveau fichier JSON s'il n'y en a pas ou si le contenu est différent
        create_new_file_if_needed(output_str, folder_name, url)

def create_new_file_if_needed(output_str, folder_name, url):
    # Obtention de tous les fichiers JSON dans le répertoire spécifié
    json_files = glob.glob(os.path.join(folder_name, '*.json'))

    if json_files:
        # Trouver le fichier le plus récent
        latest_file = max(json_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            file_content = json.load(f)
            # Comparaison du contenu du fichier avec 'output'
            if file_content['output'] != output_str:
                # Création d'un nouveau fichier si le contenu est différent
                create_new_file(output_str, folder_name, url, latest_file)
    else:
        # Création d'un nouveau fichier JSON s'il n'y en a pas
        create_new_file(output_str, folder_name, url)

def create_new_file(content, folder_name, url, last_file=None):
    # Création d'un nouveau fichier avec un nom unique dans le dossier spécifié
    new_file = os.path.join(folder_name, f"{uuid.uuid4()}.json")
    data = {
        'url': url,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'last_file_created': datetime.datetime.fromtimestamp(os.path.getctime(last_file)).strftime("%Y-%m-%d %H:%M:%S") if last_file else None,
        'output': content
    }
    with open(new_file, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Création du fichier : {new_file}")

def main():
    args = handle_args()
    update_config(args)
    search()

if __name__ == "__main__":
    main()
