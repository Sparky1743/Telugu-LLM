import requests
from bs4 import BeautifulSoup
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_links(page_number):
    url = f"https://www.vaartha.com/category/specials/career/page/{page_number}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', href=True)

    links = []
    for article in articles:
        link = article['href']
        if link.startswith('/'):
            link = f"https://www.vaartha.com{link}"
        links.append(link)
    
    return page_number, links

def save_links_to_csv(folder_path, page_number, links):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    filename = os.path.join(folder_path, f"{page_number}.csv")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Link"])
        for link in links:
            writer.writerow([link])

def process_page(folder_path, page_number):
    try:
        page_number, links = fetch_links(page_number)
        save_links_to_csv(folder_path, page_number, links)
        print(f"Page {page_number} processed successfully.")
    except Exception as e:
        print(f"An error occurred on page {page_number}: {e}")

if __name__ == "__main__":
    folder_path = '/home/llmtelugu/code/vartha/csv'
    total_pages = 34

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_page, folder_path, page_number) for page_number in range(1, total_pages + 1)]
        for future in as_completed(futures):
            future.result()  # To propagate exceptions if any
