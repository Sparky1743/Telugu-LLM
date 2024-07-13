import os
import csv
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  # Importing Retry directly from urllib3

def download_pdfs(csv_file, download_folder, counter):
    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Configure retry mechanism
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # Open the CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if it exists

        # Loop through each row in the CSV file
        for row in csv_reader:
            counter += 1
            if counter % 20 == 0:
                time.sleep(60)  # Sleep for 60 seconds every 20 requests
            pdf_url = row[0]  # Assuming the URL is in the first column
            pdf_name = pdf_url.split('/')[-1]  # Extracting the filename from the URL

            # Download the PDF file with retry mechanism
            try:
                response = session.get(pdf_url)
                response.raise_for_status()  # Raise HTTPError for bad status codes
                with open(os.path.join(download_folder, pdf_name), 'wb') as pdf_file:
                    pdf_file.write(response.content)
                print(f"Downloaded: {pdf_name}")
            except requests.exceptions.HTTPError as e:
                print(f"Failed to download {pdf_url}: {e}")

# Example usage:
csv_file = '/Users/pavandeekshith/B-Tech/TeluguLLM/output.csv'
download_folder = '/Users/pavandeekshith/B-Tech/TeluguLLM/data/data_pdfs'
counter = 0
download_pdfs(csv_file, download_folder, counter)
