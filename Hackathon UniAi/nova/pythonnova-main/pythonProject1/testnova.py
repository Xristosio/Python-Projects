from bs4 import BeautifulSoup
import requests


# Function to extract specific tags from multiple URLs
# Function to extract specific tags from multiple URLs
def extract_specific_tags_from_urls(urls, tags_to_extract):
    all_data = []

    for url in urls:
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
        all_data.append(data)

    return all_data



# List of URLs to process
urls = [
    'https://www.protothema.gr/greece/article/1444792/provlimata-sto-diktuo-tis-nova/',
    'https://www.in.gr/2023/12/12/greece/dora-prospathei-nova-na-eksagorasei-tin-anoxi-ton-syndromiton-gia-tin-katarreysi-tou-diktyou/',
    'https://www.newsit.gr/media/Nova-EON-On-Demand-ametrites-seires-kai-tainies-opote-esy-thes/3990446/',
    'https://www.kathimerini.gr/life/562898599/pos-i-nova-anavathmizei-tin-empeiria-tis-tileorasis-me-tin-ananeomeni-eon-on-demand/'
]

# Dictionary with tags to extract for each URL
# Dictionary with tags to extract for each URL
# Dictionary with tags to extract for each URL
tags_to_extract = {
    'h1': None,  # Έχει ήδη το 'h1' στο URL, οπότε None για class
    'time': None,  # Ίδιο για το 'time'
    'div': ['articleContainer__main', 'entry-content post-with-no-excerpt', 'inner-main-article', 'column p-0 entry-content content'],  # Κλάσεις div
    'p': 'main-content'
    # Μπορείς να προσθέσεις περισσότερα tags ή id αν θέλεις
}


# Extract data from each URL
result = extract_specific_tags_from_urls(urls, tags_to_extract)

# Print the extracted data
for i, data in enumerate(result, 1):
    print(f"Data from URL {i}: {data}")
