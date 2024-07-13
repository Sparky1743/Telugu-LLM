import requests
from bs4 import BeautifulSoup
import csv
import os
import threading

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract links from the specified divs
    first_big_top_card_section = soup.find('div', class_='row row_right_padding1 first-big-top-card')
    if first_big_top_card_section:
        a_tags = first_big_top_card_section.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                links.append(link)
    
    left_section = soup.find('div', class_='col-md-8 nopad1 sticky_elements_scroll left-section this-80 nopad-mobile')
    if left_section:
        a_tags = left_section.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                links.append(link)
    
    no_data_found = soup.find('p', class_='no-data-found')
    
    return links, no_data_found is None  # Also return whether "No Data Found" was found

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
            # Exclude page number from the link and prepend base URL
            link_parts = link.split('/')
            if len(link_parts) > 3 and link_parts[-1].isdigit():
                continue  # Skip links with a trailing numeric part
            link = "https://www.teluguglobal.com/" + link_parts[-1]
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
            page_url = f"{base_url}/{page}"
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
    "news": "https://www.teluguglobal.com/news",
    "more": "https://www.teluguglobal.com/more",
    "arts-literature": "https://www.teluguglobal.com/arts-literature",
    "crime": "https://www.teluguglobal.com/crime",
    "sports": "https://www.teluguglobal.com/sports",
    "women": "https://www.teluguglobal.com/women",
    "health-life-style": "https://www.teluguglobal.com/health-life-style",
    "cinema-and-entertainment": "https://www.teluguglobal.com/cinema-and-entertainment",
    "editors-choice": "https://www.teluguglobal.com/editors-choice"
}

# Base directory to save CSV files
base_directory = '/home/llmtelugu/csv_data/teluguglobal'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the main function
main(base_urls, base_directory)
