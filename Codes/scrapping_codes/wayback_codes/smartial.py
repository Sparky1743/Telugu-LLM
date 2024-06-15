import csv
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import html
import time

def extract_telugu_text_from_url(url):
    try:
        data = {
            'wurl': url,
            'extrm': 'smartial'  # Change extraction method if needed
        }
        response = requests.post('https://www.smartial.net/smart-tools/wextractor.php', data=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        telugu_text = ''
        for paragraph in paragraphs:
            text = paragraph.get_text()
            telugu_text += ' '.join(re.findall(r'([\u0C00-\u0C7F]+ *[.,?!0-9]*)', text)) + '\n'
        telugu_text = html.unescape(telugu_text)
        return telugu_text.strip()
    except Exception as e:
        print(f"Error processing URL: {url}, {e}")
        return ''

def process_link(link):
    telugu_text = extract_telugu_text_from_url(link)
    # print(f"Processing link: {link}")
    # print(telugu_text)]
    return telugu_text

def process_links_in_batches(csv_file, output_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        links = [row[0] for row in reader]

    not_found_counter = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
            futures = []
            for link in links:
                future = executor.submit(process_link, link)
                futures.append(future)
            for future in futures:
                telugu_text = future.result()
                if telugu_text:
                    outfile.write(telugu_text)
                    outfile.write('\n\n')
                else:
                    print("text not found")
                    not_found_counter += 1
                    if not_found_counter % 10 == 0 and not_found_counter != 0:
                        print(f"Reached 10 consecutive 'text not found'. Waiting for 60 seconds.")
                        time.sleep(60)
                        not_found_counter = 0 

# Example usage
def main(csv_file_path, output_file_path):
    process_links_in_batches(csv_file_path, output_file_path)

# csv_file_path = 'D:\\SSD-files\\Telugu LLM\\CSV Files\\Eenadu_links.csv'
# output_file_path = 'telugu_text_output.txt'
