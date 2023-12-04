# Scraper de Données pour BooksToScrape.com

## Description
Ce projet Python est conçu pour extraire toutes les données du site web BooksToScrape.com. Il génère un dossier /csv qui regroupe tous les fichiers csv, distincts pour chaque catégorie de livre et télécharge toutes les images des livres dans un dossier /livres automatiquement créé pour le stockage des images.

## Fonctionnalités

### Extraction de Données : 
Scrapping de toutes les informations des livres disponibles sur BooksToScrape.com, y compris le titre, le prix, la disponibilité, etc.

### Organisation par Catégorie : 
Les données sont organisées et enregistrées dans un fichier CSV distinct pour chaque catégorie de livre.

### Téléchargement d'Images : 
Télécharge les images de couverture de chaque livre et les stocke dans un dossier 'images' créé automatiquement lors de l'extraction.

## Prérequis
Python 3.11.3
Bibliothèques Python : requests, BeautifulSoup, pandas, voir le fichier requirements.

## Installation

### Clonez ce dépôt en utilisant :

git clone https://github.com/AurelienAllenic/BooksOnline---python---p1

### Installez les dépendances nécessaires :

pip install -r requirements.txt

## Usage

Pour lancer le script, exécutez :
python books.py || éxécutez le script via votre IDE

## Structure du Projet
books.py : Le script principal pour le scraping des données.
requirements.txt : Fichier contenant les dépendances nécessaires.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

