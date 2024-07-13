import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    a_tags = soup.find_all('a', href=True)
    for a_tag in a_tags:
        link = a_tag['href']
        if link not in links:
            links.append(link)
    return links

# Function to write links to CSV
def write_links_to_csv(links, csv_file_path):
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['link'])

    existing_links = set()
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and row[0] != 'link':  # Avoid adding the header to existing_links
                existing_links.add(row[0])

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            if link not in existing_links:
                print(f"Writing link to CSV: {link}")  # Debugging: Print each link being written
                writer.writerow([link])
                existing_links.add(link)

# Function to load content from a specific page
def load_page_content(url, csv_file_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        links = extract_links(html_content)
        
        # Debugging: Print the number of links found and the first few links
        print(f"Found {len(links)} links on page: {url}")
        print(f"Sample links: {links[:5]}")
        
        write_links_to_csv(links, csv_file_path)
    else:
        print(f"Failed to retrieve page: {url}")

# Test function for one category
def test_single_category(base_url, max_pages, base_directory):
    try:
        category = "news"
        print(f"Processing category: {category}")
        csv_file_path = os.path.join(base_directory, f"{category}.csv")
        
        for page in range(1, max_pages + 1):
            page_url = f"{base_url}page/{page}/" if page > 1 else base_url
            print(f"Processing page {page} of {category}")
            load_page_content(page_url, csv_file_path)
            print(f"Links from page {page} saved to {csv_file_path}")

    except Exception as e:
        print(f"An error occurred while processing {category}: {e}")

# Base URL for the category
base_url = "https://newtelugunews.com/te/"

# Maximum pages to process
max_pages = 838

# Base directory to save CSV files
base_directory = '/home/llmtelugu/csv_data/newtelugunews'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the test
test_single_category(base_url, max_pages, base_directory)
