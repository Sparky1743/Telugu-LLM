import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import hashlib
import re
import time
import random

# Function to crawl data from a single link with retries
def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            response = urllib.request.urlopen(link)
            if response.status == 200:
                return response.read()
            else:
                print(f"Failed to fetch data from {link}. Retrying...")
                retries += 1
                time.sleep(retry_interval)
        except Exception as e:
            print(f"An error occurred while fetching data from {link}: {e}. Retrying...")
            retries += 1
            time.sleep(retry_interval)
    print(f"Failed to fetch data from {link} after {max_retries} retries.")
    return None

# Function to crawl data from a single link
def crawl_data_from_link(link):
    return crawl_data_from_link_with_retry(link)

# Function to check if the text contains Telugu characters
def is_telugu(text):
    telugu_range = r'[\u0C00-\u0C7F]+'
    return re.match(telugu_range, text)

# Function to extract Telugu data from HTML content
def extract_data_from_html(html_content):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        p_elements = soup.find_all('p')

        for p in p_elements:
            p_text = p.get_text(separator=' ').strip()
            telugu_text = [text.strip() for text in p_text.split() if is_telugu(text)]
            telugu_article = ' '.join(telugu_text)
            if telugu_article:
                extracted_data.append(telugu_article)

    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

# Function to process a single link
def process_link(idx, link):
    html_content = crawl_data_from_link(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content)
        if extracted_data:
            link_hash = hashlib.sha1(link.encode('utf-8')).hexdigest()[:10]
            text_file_path = os.path.join(corpus_directory, f"document_{idx + 1}_{link_hash}.txt")

            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write('\n'.join(extracted_data))
            print(f"Extracted data from {link} and saved to {text_file_path}")
            return True
    return False

# Read CSV and process links in parallel
csv_file_path = '/home/llmtelugu/data/wayback_data/eenaducsv/12mayeenadu.csv'
corpus_directory = '/home/llmtelugu/data/wayback_data/text_data'  
encoding = 'ISO-8859-1'  

if not os.path.exists(corpus_directory):
    os.makedirs(corpus_directory)

# Load links from CSV
links = []
with open(csv_file_path, 'r', encoding=encoding) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    links = [row['link'] for row in csv_reader]

while True:
   
    failed_links = []
    counter = 0
    for idx, link in enumerate(links):
        success = process_link(idx, link)
        if not success:
            failed_links.append(link)
        counter += 1
        if counter % 20 == 0:
            # Generate a random delay between 1 and 5 seconds
            random_delay = random.uniform(1, 5)
            print(f"Waiting for {random_delay} seconds...")
            time.sleep(random_delay)

    links = failed_links

    # Check if the user wants to quit
    user_input = input("Press 'q' to quit or any other key to continue: ")
    if user_input.lower() == 'q':
        break

print("All links processed.")
