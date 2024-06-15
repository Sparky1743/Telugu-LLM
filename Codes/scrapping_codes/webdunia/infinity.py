from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU for headless
options.add_argument('--no-sandbox')  # Bypass OS security model

# Set Firefox profile preferences
driver = webdriver.Firefox(options=options)

# Function to scroll down the page gradually
def scroll_down_page(driver, scroll_step=100, delay=0.1):
    # Get current height of the page
    current_height = driver.execute_script("return document.body.scrollHeight")
    # Initialize the scroll position
    scroll_position = 0
    pages_scrolled = 0

    while scroll_position < current_height:
        # Scroll down by a certain amount
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        # Wait for a short delay
        time.sleep(delay)
        # Update the scroll position
        scroll_position += scroll_step
        pages_scrolled += 1
        print(f"Scrolled {scroll_position} pixels. Pages scrolled: {pages_scrolled}")
        # Check if CSV is updating
        if pages_scrolled % 5 == 0:  # Check after every 5 pages scrolled
            print("Checking if CSV is updating...")
            with open(output_csv, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows_count = sum(1 for row in reader)
            print(f"Rows in CSV: {rows_count}")

# Main function to scrape URLs
def scrape_urls(url, output_csv):
    driver.get(url)
    time.sleep(3)  # Give the page time to load

    with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            scroll_down_page(driver)

            a_tags = driver.find_elements(By.TAG_NAME, 'a')
            for a in a_tags:
                href = a.get_attribute('href')
                if href and href.startswith('http'):
                    csv_writer.writerow([href])
                    print(f"Appended URL: {href}")


if __name__ == "__main__":
    url = 'https://telugu.webdunia.com/valentine-day'  # Replace with the target URL
    output_csv = '/home/llmtelugu/code/webdunia/csv/vd.csv'
    scrape_urls(url, output_csv)
    print(f"URLs have been continuously saved to {output_csv}")
