import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to extract links from the specific HTML content section
def extract_links(html_content, base_url):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    print("Title:", soup.title.get_text())
    
    # Find the specific div section
    main_content_div = soup.find("div", class_="td-ss-main-content")
    if main_content_div:
        entry_titles = main_content_div.find_all("h3", class_="entry-title td-module-title")
        for entry_title in entry_titles:
            link_tag = entry_title.find("a", href=True)
            if link_tag:
                link = link_tag['href']
                links.append(link)
    else:
        print("Main content div not found.")
    return links

def fetch_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 404:
            print(f"Page not found: {url}")
            return "404"
        else:
            print(f"Failed to fetch HTML from {url} with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching HTML from {url}: {e}")
        return None

def save_links_to_csv(links, csv_file_path):
    if links:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for link in links:
                writer.writerow([link])
        print(f"Links saved to {csv_file_path}")
        
        # Remove duplicates within the CSV file
        df = pd.read_csv(csv_file_path, header=None)
        df.drop_duplicates(inplace=True)
        df.to_csv(csv_file_path, index=False, header=False)
        print(f"Duplicate rows removed from {csv_file_path}")
    else:
        print(f"No links found to save for {csv_file_path}")

def process_page(page_num, base_url, corpus_dir, link_base_url):
    if page_num == 1:
        url = base_url  # No need to append /page/{page_num} for the first page
    else:
        url = f"{base_url}/page/{page_num}"  # Append /page/{page_num} for subsequent pages
    csv_file_path = os.path.join(corpus_dir, f"{page_num}.csv")

    # Fetch HTML content
    html_content = fetch_html(url)
    if html_content == "404":
        return "404"
    if html_content:
        links = extract_links(html_content, link_base_url)
        if links:
            save_links_to_csv(links, csv_file_path)
            return None  # Successful, no need to retry
        else:
            print(f"No links found on page {page_num}.")
            return url  # No links found, exit retry loop
    else:
        print(f"Failed to fetch HTML content for page {page_num}")
        return url

def main(base_urls, page_limits, corpus_dir, max_workers=10):
    for category, url in base_urls.items():
        category_dir = os.path.join(corpus_dir, category)
        os.makedirs(category_dir, exist_ok=True)  # Create category directory if not exists

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            failed_urls = []
            futures = []
            for page_num in range(1, page_limits[category] + 1):
                print(f"Processing page {page_num} of category {category}")
                futures.append(executor.submit(process_page, page_num, url, category_dir, url))
            
            for future in as_completed(futures):
                failed_url = future.result()
                if failed_url == "404":
                    print(f"Stopping pagination for category {category} at page {page_num} due to 404 error.")
                    break
                if failed_url:
                    failed_urls.append(failed_url)
        
        failed_csv_path = os.path.join(category_dir, "failed_urls.csv")

        if failed_urls:
            print("----------------------------------------")
            print(f"Saving Failed URLs to {failed_csv_path}")
            print("----------------------------------------")
            if not os.path.isfile(failed_csv_path):
                with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
                    fieldnames = ['failed_url']
                    writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
                    writer.writeheader()

            with open(failed_csv_path, 'a', newline='', encoding='utf-8') as failed_csv:
                fieldnames = ['failed_url']
                writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
                for url in failed_urls:
                    writer.writerow({'failed_url': url})
            print("Failed URLs appended to:", failed_csv_path)

# Base URLs for each category
base_urls = {
    "crime-news": "https://www.telugumirchi.com/telugu/crime-news",    
    "movies": "https://www.telugumirchi.com/telugu/movies",
    "other-news": "https://www.telugumirchi.com/telugu/other-news",
    "reviews": "https://www.telugumirchi.com/telugu/reviews",
    "andrapradesh": "https://www.telugumirchi.com/telugu/politics/andhra-pradesh-news",
    "telangana": "https://www.telugumirchi.com/telugu/politics/telangana-news",
    "national": "https://www.telugumirchi.com/telugu/politics/national",
    "international": "https://www.telugumirchi.com/telugu/politics/international",
    "other-states": "https://www.telugumirchi.com/telugu/politics/other-states"
}

# Number of pages for each category
page_limits = {
    "crime-news": 3,
    "movies": 4835,
    "other-news": 650,
    "reviews": 55,
    "andrapradesh": 457,
    "telangana": 260,
    "national": 56,
    "international": 25,
    "other-states": 13
}

corpus_dir = '/home/llmtelugu/csv_data/telugu_mirchi'

main(base_urls, page_limits, corpus_dir, max_workers=10)
