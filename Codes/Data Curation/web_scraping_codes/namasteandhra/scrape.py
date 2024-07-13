import requests
from bs4 import BeautifulSoup
import csv
import os
import threading

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract links from 'jeg_hero_wrapper'
    hero_wrappers = soup.find_all('div', class_='jeg_hero_wrapper')
    for hero_wrapper in hero_wrappers:
        a_tags = hero_wrapper.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                links.append(link)

    # Extract links from 'jeg_block_container'
    block_containers = soup.find_all('div', class_='jeg_block_container')
    for block_container in block_containers:
        a_tags = block_container.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                links.append(link)

    return links

# Function to write links to CSV and remove duplicates
def write_links_to_csv(links, csv_file_path):
    existing_links = set()
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    existing_links.add(row[0])

    new_links = [link for link in links if link not in existing_links]

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in new_links:
            writer.writerow([link])

    print(f"Saved {len(new_links)} new links to {csv_file_path}")

# Function to write failed URLs to a CSV file
def write_failed_urls_to_csv(failed_urls, failed_csv_file_path):
    with open(failed_csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for url in failed_urls:
            writer.writerow([url])

    print(f"Saved {len(failed_urls)} failed URLs to {failed_csv_file_path}")

# Function to load content from a specific page
def load_page_content(url, csv_file_path):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        links = extract_links(html_content)
        write_links_to_csv(links, csv_file_path)
    else:
        print(f"Failed to retrieve page: {url}")
        return False  # Indicate failure
    return True  # Indicate success

# Function to process a single category
def process_category(category, base_url, max_pages, base_directory, failed_csv_file_path):
    try:
        print(f"Processing category: {category}")
        csv_file_path = os.path.join(base_directory, f"{category}.csv")
        failed_urls = []
        
        for page in range(1, max_pages + 1):
            page_url = f"{base_url}page/{page}/" if page > 1 else base_url
            print(f"Processing page {page} of {category}")
            if not load_page_content(page_url, csv_file_path):
                failed_urls.append(page_url)

        if failed_urls:
            write_failed_urls_to_csv(failed_urls, failed_csv_file_path)
        
    except Exception as e:
        print(f"An error occurred while processing {category}: {e}")

# Main function to process each category concurrently
def main(base_urls, max_pages_list, base_directory, failed_csv_file_path):
    threads = []
    for idx, (category, url) in enumerate(base_urls.items()):
        max_pages = max_pages_list[idx]
        thread = threading.Thread(target=process_category, args=(category, url, max_pages, base_directory, failed_csv_file_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# URLs for different categories with their respective max pages
base_urls = {
    "politics": "https://namasteandhra.com/category/politics/",
    "nri": "https://namasteandhra.com/category/nri/",
    "movies": "https://namasteandhra.com/category/movies/",
    "international": "https://namasteandhra.com/category/around-the-world/",
    "gallery":"https://namasteandhra.com/category/gallery/",
}

# Maximum pages for each category
max_pages_list = [740, 49, 196, 112, 30]

# Base directory to save CSV files
base_directory = '/home/llmtelugu/csv_data/namasteandhra'

# Path to save failed URLs
failed_csv_file_path = '/home/llmtelugu/code/namasteandhra/failed_csv_urls.csv'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Ensure the failed URLs file exists
if not os.path.isfile(failed_csv_file_path):
    with open(failed_csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['failed_url'])

# Run the main function
main(base_urls, max_pages_list, base_directory, failed_csv_file_path)
