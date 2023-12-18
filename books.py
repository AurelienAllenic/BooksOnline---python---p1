import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import string

def get_one_product(url):
    # Effectuer la requête HTTP
    response = requests.get(url)

    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les données nécessaires
    product_page_url = url
    title = soup.find('h1')
    if title:
        title = title.text

    # Trouver la table contenant les informations
    table = soup.find('table', class_='table-striped')
    if table:
        # Extraire les données de la table
        upc = table.find('th', string='UPC').find_next_sibling('td')
        price_including_tax = table.find('th', string='Price (incl. tax)').find_next_sibling('td')
        price_excluding_tax = table.find('th', string='Price (excl. tax)').find_next_sibling('td')
        number_available = table.find('th', string='Availability').find_next_sibling('td')
        # Si les infos sont disponibles, alors on les affecte à des variables
        if upc and price_including_tax and price_excluding_tax and number_available:
            upc = upc.text
            # On enlève le caractère 'Â' du priux en livres par ''
            price_including_tax = price_including_tax.text.replace('Â', '')
            price_excluding_tax = price_excluding_tax.text.replace('Â', '')
            number_available = number_available.text

            # Extraire la description si elle est bien trouvée
            product_description = soup.find('meta', attrs={'name': 'description'})
            if product_description:
                product_description = product_description['content']

            # Extraire la catégorie
            category = soup.find('ul', class_='breadcrumb').find_all('li')[-2].text.strip()

            # Extraire la note de l'évaluation via le nom de la class
            star_rating_element = soup.find('p', class_=re.compile('^star-rating'))
            classes = star_rating_element.get('class', [])
            rating = 0
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

            # Extraire l'URL de l'image
            image_url = soup.find('div', class_='item active').find('img')['src']

            # Données à écrire dans le fichier CSV avec retours à la ligne entre chaque info
            data = [
                f"\nproduct_page_url : {product_page_url}",
                f"\nuniversal_product_code (upc) : {upc}",
                f"\ntitle : {title}",
                f"\nprice_including_tax: {price_including_tax}",
                f"\nprice_excluding_tax: {price_excluding_tax}",
                f"\nnumber_available: {number_available}",
                f"\nproduct_description: {product_description}",
                f"\ncategory: {category}",
                f"\nreview_rating : {rating}/5",
                f"\nimage_url: {image_url}",
            ]

            return data

def get_from_category(url, category_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = soup.select('h3 a')
    category_books_data = []

    for link in product_links:
        product_url = link['href']
        product_path = product_url.rsplit('/', 2)[-2]
        product_final_url = f"https://books.toscrape.com/catalogue/{product_path}"
        book_data = get_one_product(product_final_url)
        category_books_data.append(book_data)

    pager = soup.find('ul', class_='pager')
    if pager:
        next_link = pager.find('li', class_='next')
        if next_link:
            next_page = next_link.find('a')['href']
            next_page_url = url.rsplit('/', 1)[0] + '/' + next_page
            category_books_data += get_from_category(next_page_url, category_name)

    return category_books_data

def sanitize_filename(filename):
    # Définit des caractères valides
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    # remplace les caractères spéciaux par un _
    return ''.join(c if c in valid_chars else '_' for c in filename)

def download_image(url, category_name, title, base_url='https://books.toscrape.com'):
    # Le dossier doit d'abord avoir été créé
    category_folder = f'images/{category_name}'
    os.makedirs(category_folder, exist_ok=True)

    # Modifier l'url pour qu'il correspnd aux images
    absolute_url = f'{base_url}/{url}'

    # Extraire le nom de fichier à partir du titre en le transformant pour éviter les caractères spéciaux
    image_name = f'{sanitize_filename(title)}.jpg'

    # Chemin complet du fichier image local
    local_path = os.path.join(category_folder, image_name)

    # Télécharger l'image
    response = requests.get(absolute_url)
    with open(local_path, 'wb') as file:
        file.write(response.content)

    print(f'Image enregistrée localement : {local_path}')

def get_all_categories(url):
    # Effectuer la requête HTTP
    response = requests.get(url)
    
    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver la div contenant les catégories
    categories_div = soup.find('div', class_='side_categories')

    # Trouver tous les liens à l'intérieur de la div des catégories
    category_links = categories_div.find_all('a')

    # Récupérer les URLs des catégories en excluant books
    category_urls = []
    for link in category_links:
        print(link['href'])
        if link['href'] != 'catalogue/category/books_1/index.html':
            print(f"{link['href']},  lien trouvé")
            category_url = url.rsplit('/', 1)[0] + '/' + link['href']
            category_urls.append(category_url)

    return category_urls

# URL de base
base_url = 'https://books.toscrape.com/index.html'
all_categories = get_all_categories(base_url)

for category_url in all_categories:
    category_name = category_url.rsplit('/', 2)[-2]
    category_books_data = get_from_category(category_url, category_name)

    csv_folder = 'csv'
    os.makedirs(csv_folder, exist_ok=True)
    csv_file = os.path.join(csv_folder, f'{category_name}_books.csv')

    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Product URL', 'UPC', 'Title', 'Price incl. Tax', 'Price excl. Tax', 'Availability', 'Description', 'Category', 'Rating', 'Image URL'])
        writer.writerows(category_books_data)

    for data in category_books_data:
        image_url = data[-1].split(':')[-1].strip()
        title = data[2].split(':')[-1].strip()
        download_image(image_url, category_name, title)
