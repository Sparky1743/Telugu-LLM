# from bs4 import BeautifulSoup
# import requests
# import csv
# import os
# import pandas as pd
# import time
# import random


# # Function to check if a URL is already present in the CSV
# def is_url_present(csv_file, url):
#     with open(csv_file, 'r', newline='') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row and row[0] == url:
#                 return True
#     return False

# # Add random delay to avoid request timeout
# def random_delay(min_delay, max_delay):
#     delay = random.uniform(min_delay, max_delay)
#     print(f"Waiting for {delay:.2f} seconds...")
#     time.sleep(delay)

# # Function to extract links from the specific HTML content section
# def extract_links(html_content):
#     links = []
#     soup = BeautifulSoup(html_content, "html.parser")
#     print("Title:", soup.title.get_text())
    
#     # Find the specific div section
#     main_content_div = soup.find("div", class_="td-pb-span8 td-main-content")
#     if main_content_div:
#         content_div = main_content_div.find("div", class_="td-ss-main-content")
#         if content_div:
#             a_tags = content_div.find_all('a', href=True)
#             for a in a_tags:
#                 link = a['href']
#                 # Filter out non-news URLs (adjust according to your needs)
#                 if "/tag/" not in link and "category/" not in link:
#                     links.append(link)
#     else:
#         print("Main content div not found.")
#     return links

# def fetch_html(url, max_retries=3, delay=1):
#     retries = 0
#     while retries < max_retries:
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return response.content
#             else:
#                 print(f"Failed to fetch HTML from {url} with status code {response.status_code}")
#                 return None
#         except Exception as e:
#             print(f"An error occurred while fetching HTML from {url}: {e}")
#             retries += 1
#             print(f"Retrying in {delay} seconds...")
#             time.sleep(delay)
#     print(f"Max retries exceeded for {url}.")
#     return None

# def main(burl, corpus_dir, file_name):
#     base_url = burl
#     csv_directory = corpus_dir
#     csv_file_path = os.path.join(csv_directory, f"{file_name}.csv")

#     failed_urls = []
#     if not os.path.isfile(csv_file_path):
#         with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#             fieldnames = ['link']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()

#     html_content = fetch_html(base_url)
#     if html_content:
#         links = extract_links(html_content)

#         # Write links to CSV file
#         if not is_url_present(csv_file_path, base_url):
#             with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
#                 fieldnames = ['link']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 for link in links:
#                     if not is_url_present(csv_file_path, link):
#                         writer.writerow({'link': link})
#             print(f"Links saved to {file_name}.csv")
#         else:
#             print("Base URL already exists in the CSV file.")
#     else:
#         print("Failed to fetch HTML content.")
#         random_delay(50, 60)
#         failed_urls.append(base_url)

#     still_failed = []

#     print("----------------------------------------")
#     print("Retrying Failed URLs")
#     print("----------------------------------------")
#     for url in failed_urls:
#         html_content = fetch_html(url)
#         if html_content:
#             links = extract_links(html_content)

#             # Write links to CSV file
#             if not is_url_present(csv_file_path, url):
#                 with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
#                     fieldnames = ['link']
#                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                     for link in links:
#                         if not is_url_present(csv_file_path, link):
#                             writer.writerow({'link': link})
#                 print(f"Links saved to {file_name}.csv")
#             else:
#                 print("Base URL already exists in the CSV file.")
#         else:
#             print("Failed to fetch HTML content.")
#             if len(failed_urls) < 20:
#                 random_delay(50, 60)
#             still_failed.append(url)

#     failed_csv_path = "/home/llmtelugu/data/telugu360_data/failed_urls.csv"

#     if still_failed:
#         print("----------------------------------------")
#         print(f"Saving still Failed URLs to {failed_csv_path}")
#         print("----------------------------------------")
#         if not os.path.isfile(failed_csv_path):
#             with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
#                 fieldnames = ['failed_url']
#                 writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
#                 writer.writeheader()

#         with open(failed_csv_path, 'a', newline='', encoding='utf-8') as failed_csv:
#             fieldnames = ['failed_url']
#             writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)

#             failed_csv.seek(0, os.SEEK_END)
#             if failed_csv.tell() == 0:
#                 writer.writeheader()

#             for url in still_failed:
#                 writer.writerow({'failed_url': url})
#         print("Still failed URLs appended to:", failed_csv_path)

#         fdf = pd.read_csv(csv_file_path)
#         fdf.drop_duplicates(inplace=True)
#         fdf.to_csv(csv_file_path, index=False)
#         print("Duplicate rows removed from still_failed_urls.csv")
#     else:
#         print("No URLs failed again.")

#     df = pd.read_csv(csv_file_path)
#     df.drop_duplicates(inplace=True)
#     df.to_csv(csv_file_path, index=False)
#     print(f"Cleaned data written to {file_name}.csv")

# base = "https://www.telugu360.com/te/category/politics/"
# cd = '/home/llmtelugu/data/telugu360_data/csvs'
# pn = '1'

# main(base, cd, pn)






# 2nd best code


# from bs4 import BeautifulSoup
import requests
import csv
import os
import pandas as pd
import time
import random

# Function to check if a URL is already present in the CSV
# def is_url_present(csv_file, url):
#     if not os.path.isfile(csv_file):
#         return False
#     with open(csv_file, 'r', newline='') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row and row[0] == url:
#                 return True
#     return False

# # Add random delay to avoid request timeout
# def random_delay(min_delay, max_delay):
#     delay = random.uniform(min_delay, max_delay)
#     print(f"Waiting for {delay:.2f} seconds...")
#     time.sleep(delay)

# # Function to extract links from the specific HTML content section
# def extract_links(html_content):
#     links = []
#     soup = BeautifulSoup(html_content, "html.parser")
#     print("Title:", soup.title.get_text())
    
#     # Find the specific div section
#     main_content_div = soup.find("div", class_="td-pb-span8 td-main-content")
#     if main_content_div:
#         content_div = main_content_div.find("div", class_="td-ss-main-content")
#         if content_div:
#             a_tags = content_div.find_all('a', href=True)
#             for a in a_tags:
#                 link = a['href']
#                 # Filter out non-news URLs (adjust according to your needs)
#                 if "/tag/" not in link and "category/" not in link:
#                     links.append(link)
#     else:
#         print("Main content div not found.")
#     return links

# def fetch_html(url, max_retries=3, delay=1):
#     retries = 0
#     while retries < max_retries:
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return response.content
#             else:
#                 print(f"Failed to fetch HTML from {url} with status code {response.status_code}")
#                 return None
#         except Exception as e:
#             print(f"An error occurred while fetching HTML from {url}: {e}")
#             retries += 1
#             print(f"Retrying in {delay} seconds...")
#             time.sleep(delay)
#     print(f"Max retries exceeded for {url}.")
#     return None

# def main(base_url, corpus_dir, num_pages):
#     failed_urls = []
    
#     for page_num in range(1, num_pages + 1):
#         if page_num == 1:
#             url = base_url
#         else:
#             url = f"{base_url}page/{page_num}/"
        
#         csv_file_path = os.path.join(corpus_dir, f"{page_num}.csv")

#         if not os.path.isfile(csv_file_path):
#             with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#                 fieldnames = ['link']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writeheader()

#         html_content = fetch_html(url)
#         if html_content:
#             links = extract_links(html_content)

#             # Write links to CSV file
#             with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
#                 fieldnames = ['link']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 for link in links:
#                     if not is_url_present(csv_file_path, link):
#                         writer.writerow({'link': link})
#             print(f"Links saved to {page_num}.csv")
#         else:
#             print("Failed to fetch HTML content.")
#             random_delay(50, 60)
#             failed_urls.append(url)

#     failed_csv_path = os.path.join(corpus_dir, "failed_urls.csv")

#     if failed_urls:
#         print("----------------------------------------")
#         print(f"Saving Failed URLs to {failed_csv_path}")
#         print("----------------------------------------")
#         if not os.path.isfile(failed_csv_path):
#             with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
#                 fieldnames = ['failed_url']
#                 writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
#                 writer.writeheader()

#         with open(failed_csv_path, 'a', newline='', encoding='utf-8') as failed_csv:
#             fieldnames = ['failed_url']
#             writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
#             for url in failed_urls:
#                 writer.writerow({'failed_url': url})
#         print("Failed URLs appended to:", failed_csv_path)

#     # Remove duplicates from each CSV file
#     for page_num in range(1, num_pages + 1):
#         csv_file_path = os.path.join(corpus_dir, f"{page_num}.csv")
#         if os.path.isfile(csv_file_path):
#             df = pd.read_csv(csv_file_path)
#             df.drop_duplicates(inplace=True)
#             df.to_csv(csv_file_path, index=False)
#             print(f"Duplicate rows removed from {page_num}.csv")

# base_url = "https://www.telugu360.com/te/category/politics/"
# corpus_dir = '/home/llmtelugu/data/telugu360_data/csvs'
# num_pages = 1953

# main(base_url, corpus_dir, num_pages)


from bs4 import BeautifulSoup
import requests
import csv
import os
import pandas as pd
import time
import random

# Add random delay to avoid request timeout
def random_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

# Function to extract links from the specific HTML content section
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    print("Title:", soup.title.get_text())
    
    # Find the specific div section
    main_content_div = soup.find("div", class_="td-pb-span8 td-main-content")
    if main_content_div:
        content_div = main_content_div.find("div", class_="td-ss-main-content")
        if content_div:
            a_tags = content_div.find_all('a', href=True)
            for a in a_tags:
                link = a['href']
                # Filter out non-news URLs (adjust according to your needs)
                # if "/tag/" not in link and "category/" not in link and not link.endswith('/#comments') and not link.endswith('/#respond'):
                links.append(link)
    else:
        print("Main content div not found.")
    return links

def fetch_html(url, max_retries=3, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to fetch HTML from {url} with status code {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching HTML from {url}: {e}")
            retries += 1
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"Max retries exceeded for {url}.")
    return None

def main(base_url, corpus_dir, num_pages):
    failed_urls = []
    
    for page_num in range(1, num_pages + 1):
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}page/{page_num}/"
        
        csv_file_path = os.path.join(corpus_dir, f"{page_num}.csv")

        # Fetch HTML content
        html_content = fetch_html(url)
        if html_content:
            links = extract_links(html_content)

            # Write links to CSV file
            if links:
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for link in links:
                        writer.writerow([link])
                print(f"Links saved to {page_num}.csv")
                
                # Remove duplicates within the CSV file
                df = pd.read_csv(csv_file_path, header=None)
                df.drop_duplicates(inplace=True)
                df.to_csv(csv_file_path, index=False, header=False)
                print(f"Duplicate rows removed from {page_num}.csv")
            else:
                print(f"No links found to save for {page_num}.csv")
        else:
            print("Failed to fetch HTML content.")
            random_delay(50, 60)
            failed_urls.append(url)

    failed_csv_path = os.path.join(corpus_dir, "failed_urls.csv")

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

base_url = "http://www.andhrabhoomi.net/category"
corpus_dir = '/home/llmtelugu/csv_data/andrabhoomi'
num_pages = 27003

main(base_url, corpus_dir, num_pages)
