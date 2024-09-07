import requests
from bs4 import BeautifulSoup
import re
import mysql.connector


# Σύνδεση στη βάση δεδομένων
def create_connection():
    connection = mysql.connector.connect(
        host="database-nova.c7a6a2808nfy.us-west-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="digitalsnova",
        database="nova"
    )
    return connection


# Συνάρτηση για ανάκτηση των μοναδικών συνδέσμων από μια λίστα συνδέσμων
def get_unique_links(links):
    unique_links = []
    seen_links = set()

    for link in links:
        href = link.get('href')
        if href and ('article' in href.lower() or re.search(r'\d{4,}', href)):
            if href not in seen_links:
                unique_links.append(href)
                seen_links.add(href)

    return unique_links


# Συνάρτηση για εκτύπωση των μοναδικών συνδέσμων
def print_unique_links(links):
    for link in links:
        print(f"Unique link: {link}")


# Συνάρτηση για εξαγωγή συγκεκριμένων ετικετών από πολλαπλούς συνδέσμους
def extract_specific_tags_from_urls(urls, tags_to_extract):
    all_data = []

    for url in urls:
        data = {}
        # Λήψη του περιεχομένου της σελίδας
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Εξαγωγή των συγκεκριμένων ετικετών
        for tag_name, tag_class in tags_to_extract.items():
            if tag_name == 'h1' or tag_name == 'time':
                tag_content = soup.find(tag_name)
            else:
                tag_content = soup.find(tag_name, class_=tag_class)

            data[tag_name] = tag_content.get_text(strip=True) if tag_content else None

        all_data.append(data)

    return all_data


# Συνάρτηση για αποθήκευση δεδομένων στη βάση δεδομένων
def save_data_to_database(data):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO nova_1 (h1, time, div_text) 
        VALUES (%s, %s, %s)
    """

    for entry in data:
        h1 = entry.get('h1', None)
        time = entry.get('time', None)
        div_text = entry.get('div', None)

        # Μόνο αν το div_text δεν είναι None κάνουμε την εισαγωγή
        if div_text is not None:
            cursor.execute(insert_query, (h1, time, div_text))
            connection.commit()

    cursor.close()
    connection.close()


# URLs που θέλετε να εξετάσετε
URLs = [
    'https://www.protothema.gr/tag/NOVA/',
    'https://www.in.gr/tags/nova/',
    'https://www.kathimerini.gr/search/nova/',
    'https://www.newsit.gr/tags/nova/'
]

# Ετικέτες προς εξαγωγή
tags_to_extract = {
    'h1': None,
    'time': None,
    'div': [
        'articleContainer__main',
        'entry-content post-with-no-excerpt',
        'inner-main-article',
        'column p-0 entry-content content'
    ]
}

# Εξετάζουμε κάθε URL
for URL in URLs:
    page_number = 1
    max_pages = 10 if 'newsit.gr' in URL else float('inf')  # Περιορισμός στον αριθμό των σελίδων

    while page_number <= max_pages:
        page_url = f"{URL}page/{page_number}/"
        page = requests.get(page_url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all('a')

            # Λήψη μοναδικών συνδέσμων
            unique_links = get_unique_links(links)

            # Εκτύπωση των μοναδικών συνδέσμων
            print_unique_links(unique_links)

            # Εξαγωγή δεδομένων από κάθε URL
            result = extract_specific_tags_from_urls(unique_links, tags_to_extract)

            # Αποθήκευση των εξαγομένων δεδομένων στη βάση δεδομένων
            save_data_to_database(result)

            page_number += 1  # Αυξάνουμε τον αριθμό της σελίδας
        else:
            print(f"Αποτυχία σύνδεσης στη σελίδα {page_url}.")
            break
