import os
import csv
import requests
from bs4 import BeautifulSoup
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            print(f"Processing link: {link}")
            response = requests.get(link)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to fetch data from {link}. Status code: {response.status_code}. Retrying...")
                retries += 1
                time.sleep(retry_interval)
        except Exception as e:
            print(f"An error occurred while fetching data from {link}: {e}. Retrying...")
            retries += 1
            time.sleep(retry_interval)
    print(f"Failed to fetch data from {link} after {max_retries} retries.")
    return None

def is_telugu(text):
    telugu_range = r'[\u0C00-\u0C7F]+'
    return re.match(telugu_range, text)

def extract_data_from_html(html_content):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        p_elements = soup.find_all('p')
        for p in p_elements:
            p_text = p.get_text(separator=' ').strip()
            if is_telugu(p_text):
                extracted_data.append(p_text)
    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")
    return extracted_data

def process_link_and_write(link, text_file_path):
    html_content = crawl_data_from_link_with_retry(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content)
        if extracted_data:
            try:
                with open(text_file_path, 'a', encoding='utf-8') as text_file:
                    cleaned_data = re.sub(r'\n\s*\n', '\n', '\n'.join(extracted_data)).strip()
                    text_file.write(cleaned_data + '\n\n')
                return True
            except Exception as e:
                print(f"An error occurred while writing to file {text_file_path}: {e}")
    return False

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
                links = [row[0] for row in csv_reader]

            total_links = len(links) - 1
            print(f"Processing {csv_file_name} with {total_links} links...")

            failed_links = []
            processed_links = 0

            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_link = {executor.submit(process_link_and_write, link, text_file_path): link for link in links[1:]}
                for future in as_completed(future_to_link):
                    link = future_to_link[future]
                    try:
                        success = future.result()
                        processed_links += 1
                        print(f"Processed {processed_links}/{total_links} links.")
                        if not success:
                            failed_links.append(link)
                    except Exception as e:
                        print(f"An error occurred while processing link {link}: {e}")
                        failed_links.append(link)

            if failed_links:
                for failed_link in failed_links:
                    writer.writerow({'file_name': csv_file_name, 'failed_link': failed_link})
                print(f"Failed links from {csv_file_name} stored in {failed_csv_path}")
            else:
                print(f"All URLs from {csv_file_name} processed successfully.")

csv_folder_path = r'/home/llmtelugu/code/ap7/csv'
corpus_directory = r'/home/llmtelugu/data/ap7/text_data'
failed_csv_path = r'/home/llmtelugu/code/ap7/Debug/failed_urls.csv'

process_csv_folder(csv_folder_path, corpus_directory, failed_csv_path)
