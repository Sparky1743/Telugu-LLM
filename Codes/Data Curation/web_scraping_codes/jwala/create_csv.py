from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    div = soup.find('div', class_='blog-posts hfeed')
    if div:
        a_tags = div.find_all('a', href=True)
        for a in a_tags:
            link = a['href']
            if link not in links:
                links.append(link)
    return links

# Function to write links to CSV and remove duplicates
def write_links_to_csv(links, csv_file_path):
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['link'])

    existing_links = set()
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                existing_links.add(row[0])

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            if link not in existing_links:
                writer.writerow([link])
                existing_links.add(link)

# Function to load more content by navigating to the next page
def load_more_content(driver, csv_file_path):
    page_count = 0
    while True:
        try:
            # Extract HTML content
            html_content = driver.page_source
            links = extract_links(html_content)

            # Write links to CSV file immediately after extraction
            write_links_to_csv(links, csv_file_path)

            # Find and click the "Older Posts" link
            older_posts_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.blog-pager-older-link'))
            )
            older_posts_link.click()
            page_count += 1
            print(f"Navigated to next page - {page_count}")
            time.sleep(3)  # Adjust sleep time if necessary

        except Exception as e:
            print("No more 'Older Posts' button or an error occurred:", e)
            break

# Main function
def main(base_url, csv_file_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for no GUI
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(base_url)
        time.sleep(3)  # Adjust sleep time if necessary

        load_more_content(driver, csv_file_path)

        print(f"Links saved to {csv_file_path}")

    finally:
        driver.quit()

# Base URL
base_url = "https://jwalasmusings.blogspot.com/?m=1"  # Replace with your actual URL
csv_file_path = '/Users/pavandeekshith/B-Tech/jwala/csv_data/output.csv'  # Replace with your desired CSV file path

# Run the main function
main(base_url, csv_file_path)
