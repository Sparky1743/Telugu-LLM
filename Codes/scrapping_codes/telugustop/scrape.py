import requests
from bs4 import BeautifulSoup
import csv
import os
import threading

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract links from the specified div
    band_section = soup.find('div', class_='band')
    if band_section:
        a_tags = band_section.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                # Prepend base URL to each link if it doesn't start with "http"
                if not link.startswith("http"):
                    link = f"https://telugustop.com{link}"
                links.append(link)
    
    return links, bool(band_section)

# Function to write links to CSV and remove duplicates
def write_links_to_csv(links, csv_file_path):
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['link'])

    existing_links = set()
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                existing_links.add(row[0])

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            if link not in existing_links:
                writer.writerow([link])
                existing_links.add(link)

# Function to load content from a specific page
def load_page_content(url, csv_file_path):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        links, found_target_div = extract_links(html_content)
        write_links_to_csv(links, csv_file_path)
        return found_target_div
    else:
        print(f"Failed to retrieve page: {url}")
        return False

# Function to process a single category
def process_category(category, base_url, base_directory):
    try:
        print(f"Processing category: {category}")
        csv_file_path = os.path.join(base_directory, f"{category}.csv")
        
        consecutive_empty_pages = 0
        page = 1
        while True:
            page_url = f"{base_url}/page/{page}?desktop=yes"
            print(f"Processing page {page} of {category}")
            found_target_div = load_page_content(page_url, csv_file_path)
            if not found_target_div:
                consecutive_empty_pages += 1
                if consecutive_empty_pages >= 3:
                    print(f"No data found in {consecutive_empty_pages} consecutive pages. Stopping.")
                    break
            else:
                consecutive_empty_pages = 0
            print(f"Links from page {page} saved to {csv_file_path}")
            page += 1

    except Exception as e:
        print(f"An error occurred while processing {category}: {e}")

# Main function to process each category concurrently
def main(base_urls, base_directory):
    threads = []
    for category, url in base_urls.items():
        thread = threading.Thread(target=process_category, args=(category, url, base_directory))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# URLs for different categories
base_urls = {
    "news": "https://telugustop.com/telugu/daily-update-categories/telugu-andhra-telangana-tollywood-latest-political-movie-celebrity-live-news-updates-mobile-website",
}

# Base directory to save CSV files
base_directory = '/home/llmtelugu/csv_data/telugustop'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the main function
main(base_urls, base_directory)
