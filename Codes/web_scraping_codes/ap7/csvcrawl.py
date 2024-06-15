import requests
from bs4 import BeautifulSoup
import csv
import os
import time

def fetch_links(page_number):
    url = f"https://www.ap7am.com/bhakti-articles/all?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', href=True)

    links = []
    for article in articles:
        link = article['href']
        if link.startswith('/'):
            link = f"https://www.ap7am.com{link}"
        links.append(link)
    
    return links

def save_links_to_csv(folder_path, page_number, links):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    filename = os.path.join(folder_path, f"{page_number}.csv")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Link"])
        for link in links:
            writer.writerow([link])

if __name__ == "__main__":
    folder_path = '/home/llmtelugu/code/ap7/csv'
    total_pages = 43
    for page_number in range(1, total_pages + 1):
        try:
            links = fetch_links(page_number)
            save_links_to_csv(folder_path, page_number, links)
            print(f"Page {page_number} processed successfully.")
        except Exception as e:
            print(f"An error occurred on page {page_number}: {e}")
            continue
