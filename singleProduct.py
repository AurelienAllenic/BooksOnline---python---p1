import requests
from bs4 import BeautifulSoup
import csv
import re

# URL de la page à scraper
url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

# Effectuer la requête HTTP
response = requests.get(url)

# Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extraire les données nécessaires
title = soup.find('h1').text
price = soup.find('p', class_='price_color').text
availability = soup.find('p', class_='instock availability').text.strip()
## Trouver la table contenant l'UPC
table = soup.find('table', class_='table-striped')
upc = table.find('th', string='UPC').find_next_sibling('td').text  # Extraire l'UPC
type = table.find('th', string='Product Type').find_next_sibling('td').text  # Extraire le type
reviews = table.find('th', string='Number of reviews').find_next_sibling('td').text  # Extraire le nombre de critiques

# Gestion du rating
star_rating_element = soup.find('p', class_=re.compile('^star-rating'))
classes = star_rating_element.get('class', [])
# Initialiser la note à 0
rating = 0
#### Vérifier si la liste des classes contient une classe indiquant le nombre d'étoiles
if 'One' in classes:
    rating = 1
elif 'Two' in classes:
    rating = 2
elif 'Three' in classes:
    rating = 3
elif 'Four' in classes:
    rating = 4
elif 'Five' in classes:
    rating = 5

# Product Description

description = soup.find('div', id='product_description').find_next_sibling('p').text

# Product Type

product_type = soup.find('th', string='Product Type').find_next_sibling('td').text

#### Données à écrire dans le fichier CSV, avec l'UPC formaté
data = {
    'Title': f"Title: {title}",
    'Price': f"Price: {price.replace('Â£', '£')}",
    'Availability': f"Availability: {availability}",
    'Rating': f"Rating: {rating}/5",
    'UPC': f"UPC: {upc}",
    'Product type': f"Product type: {product_type}",
    'Reviews': f"Reviews: {reviews}",
    'Description': f"Description: {description}", 
}

# Nom du fichier CSV
csv_file = 'single_product.csv'

# Écrire les données dans un fichier CSV
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

print(f'Données enregistrées dans {csv_file}: {title}, {price}, {availability}, {rating}, {upc}, {product_type}, {reviews}, {description}')
