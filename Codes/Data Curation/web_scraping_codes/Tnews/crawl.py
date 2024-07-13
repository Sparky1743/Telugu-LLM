import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to crawl data from a single link with retries
def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
    retries = 0
    ssl_context = ssl._create_unverified_context()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    while retries < max_retries:
        try:
            print(f"Attempting to fetch data from {link}, attempt {retries + 1}")
            req = urllib.request.Request(link, headers=headers)
            response = urllib.request.urlopen(req, context=ssl_context)
            if response.status == 200:
                print(f"Successfully fetched data from {link}")
                return response.read()
            elif response.status == 409:
                print(f"Conflict error (409) while fetching data from {link}. No retry will be attempted.")
                return None
            else:
                print(f"Failed to fetch data from {link}. Status code: {response.status}. Retrying...")
                retries += 1
                time.sleep(retry_interval)
        except urllib.error.HTTPError as e:
            if e.code == 409:
                print(f"Conflict error (409) while fetching data from {link}. No retry will be attempted.")
                return None
            else:
                print(f"An HTTP error occurred while fetching data from {link}: {e}. Retrying...")
                retries += 1
                time.sleep(retry_interval)
        except Exception as e:
            print(f"An error occurred while fetching data from {link}: {e}. Retrying...")
            retries += 1
            time.sleep(retry_interval)
    print(f"Failed to fetch data from {link} after {max_retries} retries.")
    return None

# Function to check if the text contains Telugu characters
def is_telugu(text):
    telugu_range = r'[\u0C00-\u0C7F]+'
    return re.search(telugu_range, text)

# Function to extract Telugu data from HTML content
def extract_data_from_html(html_content):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        # Find all paragraphs
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            # Check if the paragraph contains any Telugu text
            if is_telugu(paragraph.text):
                extracted_data.append(paragraph.text.strip())
    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

# Function to process all links in a CSV file and write extracted text to a text file
def process_csv(csv_file_path, text_file_path):
    with open(csv_file_path, 'r', encoding='ISO-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file)
        links = [row[0] for row in csv_reader]

    with open(text_file_path, 'a', encoding='utf-8') as text_file:
        for link in links:
            html_content = crawl_data_from_link_with_retry(link)
            if html_content:
                extracted_data = extract_data_from_html(html_content)
                if extracted_data:
                    # Print the first line of extracted text
                    if extracted_data:
                        print(f"First line from {link}: {extracted_data[0]}")
                    text_file.write('\n'.join(extracted_data) + '\n')


# Function to process all CSV files in a directory
def process_csv_folder(csv_folder_path, text_files_folder, failed_csv_path):
    if not os.path.exists(text_files_folder):
        os.makedirs(text_files_folder)

    with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
        fieldnames = ['file_name', 'failed_link']
        writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
        writer.writeheader()

        for csv_file_name in os.listdir(csv_folder_path):
            if csv_file_name.endswith('.csv'):
                csv_file_path = os.path.join(csv_folder_path, csv_file_name)
                text_file_path = os.path.join(text_files_folder, os.path.splitext(csv_file_name)[0] + '.txt')
                try:
                    process_csv(csv_file_path, text_file_path)
                except Exception as e:
                    writer.writerow({'file_name': csv_file_name, 'failed_link': str(e)})
                    print(f"Failed to process CSV file {csv_file_name}: {e}")
                else:
                    print(f"Successfully processed CSV file {csv_file_name}")

# Folder containing the CSV files
csv_folder_path = '/Users/pavandeekshith/B-Tech/Tnews/csv_data'  # Update with your CSV folder path
# Directory to save the text files
text_files_folder = '/Users/pavandeekshith/B-Tech/Tnews/data'  # Update with your text data folder path
# Provide the path for the failed.csv file
failed_csv_path = '/Users/pavandeekshith/B-Tech/Tnews/failed_urls.csv'


process_csv_folder(csv_folder_path, text_files_folder, failed_csv_path)