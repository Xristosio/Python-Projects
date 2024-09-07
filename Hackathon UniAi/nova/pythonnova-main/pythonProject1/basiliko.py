from bs4 import BeautifulSoup
import requests
import re

# Συνάρτηση για εξαγωγή του αριθμού της επόμενης σελίδας
def extract_next_page_number(link):
    match = re.search(r'/page/(\d+)/$', link)
    if match:
        return int(match.group(1))
    return None

# Συνάρτηση για ανάκτηση των μοναδικών συνδέσμων από μια λίστα συνδέσμων
def get_unique_links(links):
    unique_links = []
    seen_links = set()  # Δημιουργούμε ένα σύνολο για να κρατάμε τους μοναδικούς συνδέσμους

    for link in links:
        href = link.get('href')
        if href and ('article' in href.lower() or re.search(r'\d{4,}', href)):
            if href not in seen_links:  # Ελέγχουμε αν ο σύνδεσμος έχει ήδη εμφανιστεί
                unique_links.append(href)
                seen_links.add(href)  # Προσθέτουμε τον σύνδεσμο στο σύνολο των εμφανισθέντων

    return unique_links

# Συνάρτηση για εκτύπωση των μοναδικών συνδέσμων
def print_unique_links(links):
    for link in links:
        print(link)

# Συνάρτηση για εξαγωγή συγκεκριμένων ετικετών από πολλαπλούς συνδέσμους
def extract_specific_tags_from_urls(urls, tags_to_extract, source_site):
    all_data = []

    for url, site in zip(urls, source_site):
        data = {}
        # Fetch the page content
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract specified tags
        for tag_name, tag_class in tags_to_extract.items():
            # Find the tag
            if tag_name == 'h1' or tag_name == 'time':
                tag_content = soup.find(tag_name)
            else:
                tag_content = soup.find(tag_name, class_=tag_class)
            # Check if the tag exists before getting its text
            data[tag_name] = tag_content.get_text(strip=True) if tag_content else None

        # Append the data to the results list
        data["source_site"] = site
        all_data.append(data)

    return all_data

# Συνδέσμους που θέλετε να εξετάσετε
URLs = ['https://www.protothema.gr/tag/NOVA/', 'https://www.in.gr/tags/nova/',
        'https://www.kathimerini.gr/search/nova/', 'https://www.newsit.gr/tags/nova/']

# Dictionary with tags to extract for each URL
tags_to_extract = {
    'h1': None,  # Έχει ήδη το 'h1' στο URL, οπότε None για class
    'time': None,  # Ίδιο για το 'time'
    'div': ['articleContainer__main', 'entry-content post-with-no-excerpt', 'inner-main-article', 'column p-0 entry-content content'],  # Κλάσεις div
    'p': 'main-content'
    # Μπορείτε να προσθέσετε περισσότερα tags ή id αν θέλετε
}

# Οι πηγές των συνδέσμων
source_sites = ['ProtoThema', 'in.gr', 'Kathimerini', 'Newsit']

for URL, source_site in zip(URLs, source_sites):
    page_number = 1
    max_pages = 10 if 'newsit.gr' in URL else float('inf')  # Ορίζουμε το μέγιστο αριθμό σελίδων
    while page_number <= max_pages:
        page_url = f"{URL}page/{page_number}/"
        page = requests.get(page_url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all('a')
            unique_links = get_unique_links(links)

            # Extract data from each URL
            result = extract_specific_tags_from_urls(unique_links, tags_to_extract, [source_site] * len(unique_links))

            # Print the extracted data
            for i, data in enumerate(result, 1):
                print(f"Data from {data['source_site']} - URL {i}: {data}")

            page_number += 1  # Αυξάνουμε τον αριθμό της σελίδας
        else:
            print(f"Αποτυχία σύνδεσης στη σελίδα {page_url}.")
            break
