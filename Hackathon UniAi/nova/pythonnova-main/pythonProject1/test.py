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


# Συνδέσμους που θέλετε να εξετάσετε
URLs = ['https://www.protothema.gr/tag/NOVA/', 'https://www.in.gr/tags/nova/',
        'https://www.kathimerini.gr/search/nova/', 'https://www.newsit.gr/tags/nova/']

for URL in URLs:
    page_number = 1
    max_pages = 10 if 'newsit.gr' in URL else float('inf')  # Ορίζουμε το μέγιστο αριθμό σελίδων
    while page_number <= max_pages:
        page_url = f"{URL}page/{page_number}/"
        page = requests.get(page_url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all('a')
            unique_links = get_unique_links(links)

            print(f"Μοναδικοί σύνδεσμοι από τη σελίδα {page_url}:")
            print_unique_links(unique_links)

            page_number += 1  # Αυξάνουμε τον αριθμό της σελίδας
        else:
            print(f"Αποτυχία σύνδεσης στη σελίδα {page_url}.")
            break
