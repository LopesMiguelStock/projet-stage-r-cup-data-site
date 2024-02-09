
# Project Title

Ce script permet de récupérer un point précis d'une page web afin d'automatiser la récupération d'information.
## Installation

**windows et Linux**

Installation du projet avec wget
```
  wget "lien"
```
```
  cd nom-du-projet
```
```
  pip install -r requirement.txt
```
<span style="color:red">**Attention pour que le script fonctionne il faut avoir Google Chrome d'installé sur votre pc ou serveur**</span>

## Fonctionnement
Pour modifier la configuration aller dans le fichier config.json ou utiliser les commandes ci-dessous (modifie aussi le fichier config.json)
```
python main.py [-h] [-u] [-t] [-c] [-i] [-a] [-p] [-x] [-d]
```
```
-h, --help        show this help message and exit
-u, --url         URL à utiliser. Exemple : "https://exemple.com/"
-t, --tag         Balise HTML à utiliser. Exemple : "div" ou "span", etc
-c, --class_name  Classe CSS à utiliser. Exemple : "maClass"
-i, --id          ID HTML à utiliser. Exemple : "monID"
-a, --all         Trouver toutes les classes ou ID. Utilisez "yes" ou "no"
-p, --proxy       Utiliser un proxy. Utilisez "yes" ou "no"
-x, --proxy_url   URL du proxy à utiliser. Exemple : "https://corsproxy.io/?" (optionnel)
-d, --directory   Dossier à utiliser. Exemple : "monDossier"
```
**Attention à selectionner soit l'id ou la classe mais pas les deux en même temps !**