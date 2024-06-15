import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        p_elements = soup.find_all('p', class_='rtejustify')

        for p in p_elements:
            p_text = p.get_text(separator=' ').strip()
            telugu_text = [text.strip() for text in p_text.split() if is_telugu(text)]
            telugu_article = ' '.join(telugu_text)
            if telugu_article:
                extracted_data.append(telugu_article)

    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

# Function to process a single link and append data to a text file
def process_link(link, text_file):
    html_content = crawl_data_from_link(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content)
        if extracted_data:
            print(f"Writing data from {link} into {text_file}\n")
            with open(text_file, 'a', encoding='utf-8') as f:
                f.write('\n'.join(extracted_data) + '\n\n')  # Add an extra newline character
            return True
    return False

# Function to save failed links to a CSV file
def save_failed_links(failed_links, failed_links_file):
    print(f"Saving failed links to {failed_links_file}")
    with open(failed_links_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['link'])
        for link in failed_links:
            csvwriter.writerow([link])

# Function to process a single CSV file
def process_csv_file(file_path, corpus_directory, failed_links_file, encoding='ISO-8859-1'):
    print(f"Processing CSV file: {file_path}")
    links = []
    with open(file_path, 'r', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        links = [row['link'] for row in csv_reader]

    # Create a unique filename based on the CSV file name
    csv_filename = os.path.splitext(os.path.basename(file_path))[0]
    text_file_path = os.path.join(corpus_directory, f"{csv_filename}.txt")

    # Check if the text file already exists
    if os.path.exists(text_file_path):
        print(f"File {text_file_path} already exists. Skipping processing.")
        return

    failed_links = []
    counter = 0
    for idx, link in enumerate(links):
        print(f"Processing URL {idx + 1}/{len(links)}: {link}")
        success = process_link(link, text_file_path)
        if not success:
            failed_links.append(link)
        counter += 1
        if counter % 20 == 0:
            # Generate a random delay between 1 and 5 seconds
            random_delay = random.uniform(1, 5)
            print(f"Waiting for {random_delay} seconds...")
            time.sleep(random_delay)

    if failed_links:
        save_failed_links(failed_links, failed_links_file)

    print("All links processed.")

# Function to process all CSV files in the directory in parallel
def process_all_csv_files(csv_directory, corpus_directory, failed_links_directory, encoding='ISO-8859-1'):
    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(csv_directory, filename)
                failed_links_file = os.path.join(failed_links_directory, f"failed_links_{os.path.splitext(filename)[0]}.csv")
                futures.append(executor.submit(process_csv_file, file_path, corpus_directory, failed_links_file, encoding))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred during processing: {e}")

# Directories
csv_directory = '/home/llmtelugu/data/sakshi_data/csv'
corpus_directory = '/home/llmtelugu/data/sakshi_data/text_data'
failed_links_directory = '/home/llmtelugu/data/sakshi_data/Debug/failed'
encoding = 'ISO-8859-1'

# Create the failed links directory if it doesn't exist
if not os.path.exists(failed_links_directory):
    os.makedirs(failed_links_directory)

# Process all CSV files
process_all_csv_files(csv_directory, corpus_directory, failed_links_directory, encoding)
