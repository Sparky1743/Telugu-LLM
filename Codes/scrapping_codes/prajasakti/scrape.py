# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
# import csv
# import os

# # Function to extract links from the HTML content
# def extract_links(html_content):
#     links = []
#     soup = BeautifulSoup(html_content, "html.parser")
#     divs = soup.find_all('div', class_='mg-blog-thumb back-img md')
#     for div in divs:
#         a_tag = div.find('a', href=True)
#         if a_tag:
#             link = a_tag['href']
#             if link not in links:
#                 links.append(link)
#     return links

# # Function to write links to CSV and remove duplicates
# def write_links_to_csv(links, csv_file_path):
#     if not os.path.isfile(csv_file_path):
#         with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['link'])

#     existing_links = set()
#     with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             if row:
#                 existing_links.add(row[0])

#     with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         for link in links:
#             if link not in existing_links:
#                 writer.writerow([link])
#                 existing_links.add(link)

# # Function to load more content by clicking the "Load More" button
# def load_more_content(driver, csv_file_path):
#     load_more_count = 0
#     while True:
#         try:
#             load_more_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.alm-load-more-btn'))
#             )
#             # Scroll into view and click the button using JavaScript to avoid interception
#             driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
#             driver.execute_script("arguments[0].click();", load_more_button)
#             load_more_count += 1
#             print(f"Load more clicked - {load_more_count}")
#             time.sleep(3)  # Adjust sleep time if necessary

#             # Extract HTML content after loading more content
#             html_content = driver.page_source
#             links = extract_links(html_content)

#             # Write links to CSV file immediately after extraction
#             write_links_to_csv(links, csv_file_path)

#         except Exception as e:
#             print("No more 'Load More' button or an error occurred:", e)
#             break

# # Main function
# def main(base_url, csv_file_path):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Run in headless mode for no GUI
#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get(base_url)
#         time.sleep(3)  # Adjust sleep time if necessary

#         load_more_content(driver, csv_file_path)

#         print(f"Links saved to {csv_file_path}")

#     finally:
#         driver.quit()

# # Base URL
# base_url = "https://prajasakti.com/category/arogyam"  # Replace with your actual URL
# csv_file_path = '/Users/pavandeekshith/B-Tech/prajasakti/csv_data/arogyam/output.csv'  # Replace with your desired CSV file path

# # Run the main function
# main(base_url, csv_file_path)


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
# import csv
# import os

# # Function to extract links from the HTML content
# def extract_links(html_content):
#     links = []
#     soup = BeautifulSoup(html_content, "html.parser")
#     divs = soup.find_all('div', class_='mg-blog-thumb back-img md')
#     for div in divs:
#         a_tag = div.find('a', href=True)
#         if a_tag:
#             link = a_tag['href']
#             if link not in links:
#                 links.append(link)
#     return links

# # Function to write links to CSV and remove duplicates
# def write_links_to_csv(links, csv_file_path):
#     if not os.path.isfile(csv_file_path):
#         with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['link'])

#     existing_links = set()
#     with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             if row:
#                 existing_links.add(row[0])

#     with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         for link in links:
#             if link not in existing_links:
#                 writer.writerow([link])
#                 existing_links.add(link)

# # Function to load more content by clicking the "Load More" button
# def load_more_content(driver, csv_file_path):
#     load_more_count = 0
#     while True:
#         try:
#             load_more_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.alm-load-more-btn'))
#             )
#             # Scroll into view and click the button using JavaScript to avoid interception
#             driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
#             driver.execute_script("arguments[0].click();", load_more_button)
#             load_more_count += 1
#             print(f"Load more clicked - {load_more_count}")
#             time.sleep(3)  # Adjust sleep time if necessary

#             # Extract HTML content after loading more content
#             html_content = driver.page_source
#             links = extract_links(html_content)

#             # Write links to CSV file immediately after extraction
#             write_links_to_csv(links, csv_file_path)

#         except Exception as e:
#             print("No more 'Load More' button or an error occurred:", e)
#             break

# # Main function to process each category
# def main(base_urls, base_directory):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Run in headless mode for no GUI
#     driver = webdriver.Chrome(options=options)

#     try:
#         for category, url in base_urls.items():
#             print(f"Processing category: {category}")
#             csv_file_path = os.path.join(base_directory, f"{category}.csv")
#             driver.get(url)
#             time.sleep(3)  # Adjust sleep time if necessary

#             load_more_content(driver, csv_file_path)

#             print(f"Links saved to {csv_file_path}")

#     finally:
#         driver.quit()

# # URLs for different categories
# base_urls = {
#     "sports": "https://prajasakti.com/category/sports",
#     "entertainment": "https://prajasakti.com/category/entertainment",
#     "state": "https://prajasakti.com/category/varthalu/state",
#     "health": "https://prajasakti.com/category/arogyam",
#     "national":"https://prajasakti.com/category/varthalu/national",
#     "international":"https://prajasakti.com/category/varthalu/international",
#     "edit_page":"https://prajasakti.com/category/edit-page",
#     "business":"https://prajasakti.com/category/business",
#     "features":"https://prajasakti.com/category/features",
#     "sneha":"https://prajasakti.com/category/sneha",
#     "literature":"https://prajasakti.com/category/literature",
#     "district_news":"https://prajasakti.com/category/district-news",
#     "special":"https://prajasakti.com/category/special",
#     "arogyam":"https://prajasakti.com/category/arogyam",
#     "trending":"https://prajasakti.com/category/%e0%b0%9f%e0%b1%8d%e0%b0%b0%e0%b1%86%e0%b0%82%e0%b0%a1%e0%b0%bf%e0%b0%82%e0%b0%97%e0%b1%8d"
# }

# # Base directory to save CSV files
# base_directory = '/Users/pavandeekshith/B-Tech/prajasakti/csv_data'

# # Ensure the base directory exists
# os.makedirs(base_directory, exist_ok=True)

# # Run the main function
# main(base_urls, base_directory)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os
import threading

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    divs = soup.find_all('div', class_='mg-blog-thumb back-img md')
    for div in divs:
        a_tag = div.find('a', href=True)
        if a_tag:
            link = a_tag['href']
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

# Function to load more content by clicking the "Load More" button
def load_more_content(driver, csv_file_path):
    load_more_count = 0
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.alm-load-more-btn'))
            )
            # Scroll into view and click the button using JavaScript to avoid interception
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            driver.execute_script("arguments[0].click();", load_more_button)
            load_more_count += 1
            print(f"Load more clicked - {load_more_count}")
            time.sleep(2)  # Adjust sleep time if necessary

            # Extract HTML content after loading more content
            html_content = driver.page_source
            links = extract_links(html_content)

            # Write links to CSV file immediately after extraction
            write_links_to_csv(links, csv_file_path)

        except Exception as e:
            print("No more 'Load More' button or an error occurred:", e)
            break

# Function to process a single category
def process_category(category, url, base_directory):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for no GUI
    driver = webdriver.Chrome(options=options)

    try:
        print(f"Processing category: {category}")
        csv_file_path = os.path.join(base_directory, f"{category}.csv")
        driver.get(url)
        time.sleep(3)  # Adjust sleep time if necessary

        load_more_content(driver, csv_file_path)

        print(f"Links saved to {csv_file_path}")

    finally:
        driver.quit()

# Main function to process each category concurrently
def main(base_urls, base_directory):
    threads = []
    for category, url in base_urls.items():
        thread = threading.Thread(target=process_category, args=(category, url, base_directory))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# URLs for different categories
base_urls = {
    "sports": "https://prajasakti.com/category/sports",
    "entertainment": "https://prajasakti.com/category/entertainment",
    "state": "https://prajasakti.com/category/varthalu/state",
    "health": "https://prajasakti.com/category/arogyam",
    "national":"https://prajasakti.com/category/varthalu/national",
    "international":"https://prajasakti.com/category/varthalu/international",
    "edit_page":"https://prajasakti.com/category/edit-page",
    "business":"https://prajasakti.com/category/business",
    "features":"https://prajasakti.com/category/features",
    "sneha":"https://prajasakti.com/category/sneha",
    "literature":"https://prajasakti.com/category/literature",
    "district_news":"https://prajasakti.com/category/district-news",
    "special":"https://prajasakti.com/category/special",
    "arogyam":"https://prajasakti.com/category/arogyam",
    "trending":"https://prajasakti.com/category/%e0%b0%9f%e0%b1%8d%e0%b0%b0%e0%b1%86%e0%b0%82%e0%b0%a1%e0%b0%bf%e0%b0%82%e0%b0%97%e0%b1%8d"
}

# Base directory to save CSV files
base_directory = '/Users/pavandeekshith/B-Tech/prajasakti/csv_data'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the main function
main(base_urls, base_directory)
