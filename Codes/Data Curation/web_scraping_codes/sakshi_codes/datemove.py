from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import random
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import pandas as pd
import os
import csv

# Function to check if a URL is already present in the CSV
def is_url_present(csv_file, url):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == url:
                return True
    return False

# Add random delay to avoid request time out
def random_delay(min_sec, max_sec):
    rd = random.uniform(min_sec, max_sec)
    print(f"Waiting for {rd} seconds...")
    time.sleep(rd)

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    print("Title:", soup.title.get_text())
    a_tags = soup.find_all('a', href=True)
    for a in a_tags:
        link = a['href']
        # Filter out non-news URLs
        if "/telugu-news/" in link or "telugu-article/" in link:
            links.append(link)
    return links

# Function to navigate to a specific date
def navigate_to_date(driver, target_date):
    # Format the target date as 'YYYY-MM-DD'
    date_str = target_date.strftime('%Y-%m-%d')
    print(date_str)
    driver.refresh()
    time.sleep(20)
    try:
        date_input = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-drupal-selector='edit-created-date']"))
        )
    except:
        print("Date input field did not become clickable.")
        driver.quit()
        exit()

    # Remove the 'max' attribute using JavaScript
    driver.execute_script("arguments[0].removeAttribute('max')", date_input)
    time.sleep(8)

    # Use JavaScript to set the desired date
    driver.execute_script("arguments[0].value = arguments[1]", date_input, date_str)
    time.sleep(8)

    # Find the submit button
    try:
        submit_button = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-drupal-selector='edit-submit-archive-content']"))
        )
    except:
        print("Submit button did not become present.")
        driver.quit()
        exit()

    # Use JavaScript to trigger a click event on the submit button
    driver.execute_script("arguments[0].click();", submit_button)

    # Optionally, you can add a delay to let the page load
    time.sleep(20)

def wait_for_page_load(driver):
    wait = WebDriverWait(driver, 30)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

# Main function
def main(base_url):
    try:
        #Start date
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        # Set up the Selenium WebDriver for Firefox
        options = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webnotifications.enabled", False)
        options.profile = profile
        driver = webdriver.Firefox(options=options)
        driver.get(base_url)
        wait_for_page_load(driver)
        # Navigate to previous dates
        for i in range(30): 
            try:

                target_date = yesterday - datetime.timedelta(days=i)
                navigate_to_date(driver, target_date)
                date_str = target_date.strftime('%Y-%m-%d')
                csv_file_path = fr'C:\Users\birud\OneDrive\Desktop\{date_str}.csv'
                print("Navigated to:", date_str)
                time.sleep(10)  
                if not os.path.isfile(csv_file_path):
                    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['link']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()

                try:
                    # Initialize variables to track CSV row count
                    prev_row_count = 0
                    unchanged_count = 0
                    
                    while True:
                        # Scroll to the "Load more" button and wait for the page to load
                        try:
                            load_more_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Load more')]"))
                            )
                            # Scroll to the button's position
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});", load_more_button)
                            random_delay(10, 15)  # Wait for the content to load after scrolling
                            load_more_button.click()
                            print("Loading more content :)")
                            random_delay(15, 20)
                        except Exception as e:
                            print(f"No more 'Load more' button found or an error occurred: {e}")
                            break

                        # Extract HTML content after loading more content
                        html_content = driver.page_source
                        links = extract_links(html_content)

                        # Write links to CSV file
                        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                            fieldnames = ['link']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            for link in links:
                                if not is_url_present(csv_file_path, link):
                                    writer.writerow({'link': link})

                        print(f"Links saved to {date_str}.csv")
                        break
                        
                        # Check the number of rows in the CSV file
                        df = pd.read_csv(csv_file_path)
                        current_row_count = len(df)

                        # Determine if the loading process should stop
                        if current_row_count == prev_row_count:
                            unchanged_count += 1
                            if unchanged_count >= 5:
                                print("No new links found in 5 consecutive loads. Stopping.")
                                break
                        else:
                            unchanged_count = 0

                        prev_row_count = current_row_count

                except:
                    print(f"Failed to extract urls from {date_str}")

                # Clean up duplicates
                finally:
                    df = pd.read_csv(csv_file_path)
                    df.drop_duplicates(inplace=True)
                    df.to_csv(csv_file_path, index=False)
                    print(f"Cleaned data written to {date_str}.csv")
                    driver.delete_all_cookies()
                    driver.refresh()
                    time.sleep(10)

            except Exception as e:
                print(f"An error occurred in iteration {i + 1}: {e}")


    finally:
        driver.quit()

# Base URL
base_url = "https://www.sakshi.com/archive"

# Run the main function
main(base_url)
