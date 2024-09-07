from bs4 import BeautifulSoup
import requests

# Συνάρτηση για την ανάκτηση όλων των tags από μια δεδομένη σελίδα URL
def get_all_tags(URL):
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.find_all()
    else:
        print("Αποτυχία σύνδεσης στη σελίδα.")
        return []

# Σύνδεση με τη σελίδα του protothema.gr
URL = 'https://www.protothema.gr/'
all_tags = get_all_tags(URL)

# Εκτύπωση όλων των tags που βρέθηκαν στη σελίδα
for tag in all_tags:
    print(tag.name)
