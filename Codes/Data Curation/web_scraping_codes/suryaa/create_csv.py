

# import os
# import time
# import random
# import requests
# import csv
# import pandas as pd
# from bs4 import BeautifulSoup
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # Add random delay to avoid request timeout
# def random_delay(min_delay, max_delay):
#     delay = random.uniform(min_delay, max_delay)
#     print(f"Waiting for {delay:.2f} seconds...")
#     time.sleep(delay)

# # Function to extract links from the specific HTML content section
# def extract_links(html_content, base_url):
#     links = []
#     soup = BeautifulSoup(html_content, "html.parser")
#     print("Title:", soup.title.get_text())
    
#     # Find the specific div section
#     main_content_div = soup.find("div", class_="col-lg-12 col-md-12")
#     if main_content_div:
#         media_bodies = main_content_div.find_all("div", class_="media-body")
#         for media_body in media_bodies:
#             link_tag = media_body.find("a", href=True)
#             if link_tag:
#                 link = link_tag['href']
#                 full_link = link if link.startswith("http") else f"{base_url}/{link}"
#                 links.append(full_link)
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

# def save_links_to_csv(links, csv_file_path):
#     if links:
#         with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             for link in links:
#                 writer.writerow([link])
#         print(f"Links saved to {csv_file_path}")
        
#         # Remove duplicates within the CSV file
#         df = pd.read_csv(csv_file_path, header=None)
#         df.drop_duplicates(inplace=True)
#         df.to_csv(csv_file_path, index=False, header=False)
#         print(f"Duplicate rows removed from {csv_file_path}")
#     else:
#         print(f"No links found to save for {csv_file_path}")

# def process_page(page_num, base_url, category_dir, link_base_url):
#     if page_num == 1:
#         url = base_url
#     else:
#         url = f"{base_url}?pagination={page_num}"

#     csv_file_path = os.path.join(category_dir, f"{page_num}.csv")

#     # Fetch HTML content
#     html_content = fetch_html(url)
#     if html_content:
#         links = extract_links(html_content, link_base_url)
#         if not links:
#             print(f"No links found on page {page_num}. Stopping pagination.")
#             return "stop"
#         save_links_to_csv(links, csv_file_path)
#     else:
#         print(f"Failed to fetch HTML content for page {page_num}")
#         random_delay(50, 60)
#         return url
#     return None

# def main(categories, corpus_dir, max_workers=10):
#     failed_urls = []

#     for category, base_url in categories.items():
#         category_dir = os.path.join(corpus_dir, category)
#         os.makedirs(category_dir, exist_ok=True)
#         link_base_url = "https://telugu.suryaa.com"

#         page_num = 1
#         stop_pagination = False

#         while not stop_pagination:
#             with ThreadPoolExecutor(max_workers=max_workers) as executor:
#                 future_to_page = {executor.submit(process_page, page_num, base_url, category_dir, link_base_url): page_num}
                
#                 for future in as_completed(future_to_page):
#                     try:
#                         result = future.result()
#                         if result == "stop":
#                             print(f"Stopping pagination for {category} at page {page_num}")
#                             stop_pagination = True
#                         elif result:
#                             failed_urls.append(result)
#                     except Exception as exc:
#                         print(f"Page {page_num} generated an exception: {exc}")
#                         failed_urls.append(f"{base_url}?pagination={page_num}")

#                 page_num += 1

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

# categories = {
#     "movie-reviews": "https://telugu.suryaa.com/latest-movie-reviews.php",
#     "telangana": "https://telugu.suryaa.com/telangana-latest.html",
#     "andrapradesh": "https://telugu.suryaa.com/andhrapradesh-latest-news.html",
#     "national": "https://telugu.suryaa.com/national-news-in-telugu.html",
#     "sports": "https://telugu.suryaa.com/breaking-sports-news-headlines.php",
#     "international": "https://telugu.suryaa.com/international-news-in-telugu.html",
#     "crime": "https://telugu.suryaa.com/latest-crime-news-updates.php",
#     "tollywood": "https://telugu.suryaa.com/tollywood-latest-cinema-news.php",
#     "bollywood": "https://telugu.suryaa.com/bollywood-latest-cinema-news.php",
#     "life-style": "https://telugu.suryaa.com/latest-life-style-news-updates.php",
#     "astrology": "https://telugu.suryaa.com/today-astrology-news-daily-horoscope.php",
#     "education": "https://telugu.suryaa.com/education-and-career-news.php",
#     "devotion": "https://telugu.suryaa.com/devotion-bhakthi.php",
#     "business": "https://telugu.suryaa.com/business-news-stock-markets.php",
#     "technology": "https://telugu.suryaa.com/latest-technology-news.php",
#     "beauty": "https://telugu.suryaa.com/health-and-beauty-news.php",
#     "song-lyrics": "https://telugu.suryaa.com/telugu-song-lyrics.php"
# }

# corpus_dir = '/home/llmtelugu/csv_data/suryaa'

# main(categories, corpus_dir, max_workers=10)

import os
import time
import random
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add random delay to avoid request timeout
def random_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

# Function to extract links from the specific HTML content section
def extract_links(html_content, base_url):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    print("Title:", soup.title.get_text())
    
    # Find the specific div section
    main_content_div = soup.find("div", class_="col-lg-12 col-md-12")
    if main_content_div:
        media_bodies = main_content_div.find_all("div", class_="media-body")
        for media_body in media_bodies:
            link_tag = media_body.find("a", href=True)
            if link_tag:
                link = link_tag['href']
                full_link = link if link.startswith("http") else f"{base_url}/{link}"
                links.append(full_link)
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

def process_page(page_num, base_url, category_dir, link_base_url):
    if page_num == 1:
        url = base_url
    else:
        url = f"{base_url}?pagination={page_num}"

    csv_file_path = os.path.join(category_dir, f"{page_num}.csv")

    # Fetch HTML content
    html_content = fetch_html(url)
    if html_content:
        links = extract_links(html_content, link_base_url)
        if not links:
            print(f"No links found on page {page_num}.")
            return "no_links"
        save_links_to_csv(links, csv_file_path)
    else:
        print(f"Failed to fetch HTML content for page {page_num}")
        random_delay(50, 60)
        return url
    return None

def main(categories, corpus_dir, max_workers=10):
    failed_urls = []

    for category, base_url in categories.items():
        category_dir = os.path.join(corpus_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        link_base_url = "https://telugu.suryaa.com"

        page_num = 1
        consecutive_no_links = 0

        while True:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_page = {executor.submit(process_page, page_num, base_url, category_dir, link_base_url): page_num}
                
                for future in as_completed(future_to_page):
                    try:
                        result = future.result()
                        if result == "no_links":
                            consecutive_no_links += 1
                            if consecutive_no_links >= 3:
                                print(f"No links found for 3 consecutive pages in {category}. Moving to next category.")
                                break
                        else:
                            consecutive_no_links = 0
                            if result:
                                failed_urls.append(result)
                    except Exception as exc:
                        print(f"Page {page_num} generated an exception: {exc}")
                        failed_urls.append(f"{base_url}?pagination={page_num}")

                page_num += 1

            if consecutive_no_links >= 3:
                break

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

categories = {
    "movie-reviews": "https://telugu.suryaa.com/latest-movie-reviews.php",
    "telangana": "https://telugu.suryaa.com/telangana-latest.html",
    "andrapradesh": "https://telugu.suryaa.com/andhrapradesh-latest-news.html",
    "national": "https://telugu.suryaa.com/national-news-in-telugu.html",
    "sports": "https://telugu.suryaa.com/breaking-sports-news-headlines.php",
    "international": "https://telugu.suryaa.com/international-news-in-telugu.html",
    "crime": "https://telugu.suryaa.com/latest-crime-news-updates.php",
    "tollywood": "https://telugu.suryaa.com/tollywood-latest-cinema-news.php",
    "bollywood": "https://telugu.suryaa.com/bollywood-latest-cinema-news.php",
    "life-style": "https://telugu.suryaa.com/latest-life-style-news-updates.php",
    "astrology": "https://telugu.suryaa.com/today-astrology-news-daily-horoscope.php",
    "education": "https://telugu.suryaa.com/education-and-career-news.php",
    "devotion": "https://telugu.suryaa.com/devotion-bhakthi.php",
    "business": "https://telugu.suryaa.com/business-news-stock-markets.php",
    "technology": "https://telugu.suryaa.com/latest-technology-news.php",
    "beauty": "https://telugu.suryaa.com/health-and-beauty-news.php",
    "song-lyrics": "https://telugu.suryaa.com/telugu-song-lyrics.php"
}

corpus_dir = '/home/llmtelugu/csv_data/suryaa'

main(categories, corpus_dir, max_workers=10)
