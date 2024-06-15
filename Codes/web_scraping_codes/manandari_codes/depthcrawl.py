import os
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_telugu(text):
    telugu_range = r'[\u0C00-\u0C7F]+'
    return re.match(telugu_range, text)

def extract_telugu_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ptags = soup.find_all('p')
            telugu_texts = []
            for ptag in ptags:
                text = ptag.get_text().strip()
                if is_telugu(text):
                    telugu_texts.append(text)
            return telugu_texts
        else:
            print(f"Failed to fetch page: {url}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def extract_hyperlinks(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            return [link['href'] for link in links if link['href'].startswith('http')]
        else:
            print(f"Failed to fetch page: {url}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def save_telugu_text_to_file(telugu_texts, filename):
    with open(filename, 'a', encoding='utf-8') as file:  # Open the file in append mode
        for text in telugu_texts:
            cleaned_text = re.sub(r'\n+', '\n\n', text.strip())
            file.write(cleaned_text + "\n\n")
    print(f"Telugu text appended to: {filename}")

def process_link_recursive(url, filename, max_depth, current_depth=0, processed_urls=None):
    if current_depth > max_depth or url in processed_urls:
        return

    print(f"Extracting Telugu text from: {url}")
    telugu_texts = extract_telugu_text(url)
    if telugu_texts:
        save_telugu_text_to_file(telugu_texts, filename)
    else:
        print("No Telugu text found.")
    
    processed_urls.add(url)  # Mark this URL as processed
    
    print(f"Extracting hyperlinks from: {url}")
    hyperlinks = extract_hyperlinks(url)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_link_recursive, hyperlink, filename, max_depth, current_depth + 1, processed_urls) for hyperlink in hyperlinks]
        for future in as_completed(futures):
            future.result()

def process_links(main_links, directory, max_depth):
    processed_urls = set()  # Keep track of processed URLs
    with ThreadPoolExecutor() as executor:
        futures = []
        for link in main_links:
            main_filename = os.path.join(directory, link.split('/')[-1] + ".txt")
            futures.append(executor.submit(process_link_recursive, link, main_filename, max_depth, 0, processed_urls))
        for future in as_completed(futures):
            future.result()

def main():
    # List of main links
    main_links = [
        'https://manandari.com/telugu-stories-online',
        'https://manandari.com/category/charitra-history',
        'https://manandari.com/telugu-kavithalu',
        'https://manandari.com/telugu-articles',
        'https://manandari.com/category/health-tips',
        'https://manandari.com/category/our-voice-vyasalu/freedom-fighters',
        'https://manandari.com/magazine',
        'https://manandari.com/category/reviews',

        # Add more links as needed
    ]

    directory = "/home/llmtelugu/data/manandari_data/text_data"

    if not os.path.exists(directory):
        os.makedirs(directory)

    max_depth = 4  # Set the desired depth for recursive hyperlink extraction
    process_links(main_links, directory, max_depth)

if __name__ == "__main__":
    main()
