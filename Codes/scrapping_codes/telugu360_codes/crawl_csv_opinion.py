
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
    return re.search(telugu_range, text)

# Function to extract Telugu data from HTML content
def extract_data_from_html(html_content):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        p_elements = soup.find_all('p')

        for p in p_elements:
            p_text = p.get_text(separator=' ').strip()
            # Check if the paragraph contains any Telugu text
            if is_telugu(p_text):
                extracted_data.append(p_text)

    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

# Function to process a single link
def process_link(link):
    html_content = crawl_data_from_link(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content)
        return extracted_data
    return []

# Function to process all CSV files in a directory
def process_csv_folder(csv_folder_path, corpus_directory, failed_csv_path):
    if not os.path.exists(corpus_directory):
        os.makedirs(corpus_directory)

    csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
    csv_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
        fieldnames = ['file_name', 'failed_link']
        writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
        writer.writeheader()

        for csv_file_name in csv_files:
            csv_file_path = os.path.join(csv_folder_path, csv_file_name)
            text_file_path = os.path.join(corpus_directory, f"{os.path.splitext(csv_file_name)[0]}.txt")

            with open(csv_file_path, 'r', encoding='ISO-8859-1') as csv_file:
                csv_reader = csv.reader(csv_file)
                links = [row[0] for row in csv_reader]  # Read URLs from each row directly

            all_extracted_data = []
            failed_links = []
            print(f"Processing {csv_file_name}...")
            for idx, link in enumerate(links):
                print(f"Processing URL {idx + 1}/{len(links)}: {link}")
                extracted_data = process_link(link)
                if extracted_data:
                    all_extracted_data.extend(extracted_data)
                else:
                    failed_links.append(link)
                if (idx + 1) % 20 == 0:
                    random_delay = random.uniform(1, 5)
                    print(f"Waiting for {random_delay} seconds...")
                    time.sleep(random_delay)

            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write('\n'.join(all_extracted_data))
            print(f"Extracted data from {csv_file_name} saved to {text_file_path}")

            if failed_links:
                for failed_link in failed_links:
                    writer.writerow({'file_name': csv_file_name, 'failed_link': failed_link})
                print(f"Failed links from {csv_file_name} stored in {failed_csv_path}")
            else:
                print(f"All URLs from {csv_file_name} processed successfully.")

# Folder containing the CSV files
csv_folder_path = '/home/llmtelugu/data/telugu360_data/opinion/csvs'  # Update with your CSV folder path
# Directory to save the text files

corpus_directory = '/home/llmtelugu/data/telugu360_data/opinion/text'  # Update with your text data folder path

# Provide the path for the failed.csv file
failed_csv_path = '/home/llmtelugu/data/telugu360_data/opinion/failed_urls.csv'

# Call the function with the provided path
process_csv_folder(csv_folder_path, corpus_directory, failed_csv_path)
