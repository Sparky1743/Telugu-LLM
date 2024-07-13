import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract links from the specified div
    left_panel = soup.find('div', class_='oi-leftpanel')
    if left_panel:
        a_tags = left_panel.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                # Prepend base URL to each link if it doesn't start with "http"
                if not link.startswith("http"):
                    link = f"https://telugu.oneindia.com{link}"
                links.append(link)
    
    return links

# Function to write links to CSV and remove duplicates
def write_links_to_csv(links, csv_file_path):
    try:
        if not os.path.isfile(csv_file_path):
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['link'])
                print(f"Created new file and wrote header: {csv_file_path}")

        existing_links = set()
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    existing_links.add(row[0])
        print(f"Existing links loaded for {csv_file_path}")

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for link in links:
                if link not in existing_links:
                    writer.writerow([link])
                    existing_links.add(link)
                    print(f"Link {link} added to {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while writing to CSV file {csv_file_path}: {e}")

# Function to load content from a specific page
def load_page_content(session, url, csv_file_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            html_content = response.text
            links = extract_links(html_content)
            print(f"Extracted {len(links)} links from {url}")
            write_links_to_csv(links, csv_file_path)
        else:
            print(f"Failed to retrieve page: {url}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while retrieving page {url}: {e}")

# Function to process a single category
def process_category(category, base_url, max_pages, base_directory):
    try:
        print(f"Processing category: {category}")
        csv_file_path = os.path.join(base_directory, f"{category}.csv")
        
        session = requests.Session()
        
        for page in range(1, max_pages + 1):
            if page == 1:
                page_url = base_url
            else:
                page_url = f"{base_url}?page-no={page}"
            
            print(f"Processing page {page} of {category}")
            print(f"Accessing URL: {page_url}")
            load_page_content(session, page_url, csv_file_path)
            print(f"Links from page {page} saved to {csv_file_path}")
            
            # Add delay to avoid rate limiting
            time.sleep(1)  # Adjust the sleep time as needed

    except Exception as e:
        print(f"An error occurred while processing {category}: {e}")

# Main function to process each category
def main(base_urls, max_pages_list, base_directory):
    for idx, (category, url) in enumerate(base_urls.items()):
        max_pages = max_pages_list[idx]
        process_category(category, url, max_pages, base_directory)

# URLs for different categories with their respective max pages
base_urls = {
    "state": "https://telugu.oneindia.com/news/state/",
    "national": "https://telugu.oneindia.com/news/india/",
    "international": "https://telugu.oneindia.com/news/international/",
    "health": "https://telugu.oneindia.com/health/",
    "entertainment": "https://telugu.oneindia.com/entertainment/",
    "sports": "https://telugu.oneindia.com/sports/",
    "horoscope": "https://telugu.oneindia.com/jyotishyam/"
}

# Maximum pages for each category
max_pages_list = [13420, 6423, 1340, 57, 150, 37, 265]

# Base directory to save CSV files
base_directory = '/home/llmtelugu/csv_data/oneindia'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the main function
main(base_urls, max_pages_list, base_directory)
