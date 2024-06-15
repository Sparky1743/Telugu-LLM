from bs4 import BeautifulSoup
import requests
import csv
import os
import pandas as pd
import time
import random

# Function to check if a URL is already present in the CSV
def is_url_present(csv_file, url):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == url:
                return True
    return False

# Add random delay to avoid request time out
def random_delay(min, max):
    rd = random.uniform(min, max)
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
        if "/telugu-news/" in link or "/telugu-article/" in link:
            links.append(link)
    return links

# Function to scrape a section of the website
def scrape_section(base_url, field):
    return base_url + field

# Function to fetch HTML content from the URL
def fetch_html(url, max_retries=3, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to fetch HTML from {url}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching HTML from {url}: {e}")
            retries += 1
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"Max retries exceeded for {url}.")
    return None

def remove_overlapping_links(df):
    df['short_link'] = df['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1])
    df.drop_duplicates(subset='short_link', keep='first', inplace=True)
    df.drop(columns=['short_link'], inplace=True)
    return df

def clean_csv_directory(csv_directory):
    all_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    
    if len(all_files) == 1:
        print("Only one file, no need to remove duplicates")
        return
    
    all_files.sort()
    
    # Read all CSV files into DataFrames
    df_list = []
    for file in all_files:
        file_path = os.path.join(csv_directory, file)
        df = pd.read_csv(file_path)
        df['source_file'] = file  # Add a column to keep track of the source file
        df_list.append(df)
    
    # Combine all DataFrames except the latest one
    combined_df = pd.concat(df_list[:-1], ignore_index=True)
    combined_df = remove_overlapping_links(combined_df)
    
    # Get the latest file DataFrame
    latest_file = all_files[-1]
    latest_file_path = os.path.join(csv_directory, latest_file)
    latest_df = pd.read_csv(latest_file_path)
    latest_df['short_link'] = latest_df['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1])
    
    # Remove overlapping links from the latest DataFrame
    previous_links = set(combined_df['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1]))
    latest_df = latest_df[~latest_df['short_link'].isin(previous_links)]
    latest_df = latest_df.drop(columns=['short_link'])
    
    # Save the cleaned latest DataFrame back to its CSV file
    latest_df.to_csv(latest_file_path, index=False)
    print(f"Cleaned data written to {latest_file}")
    
    # Remove 'source_file' column and save back the previous DataFrames
    for df in df_list[:-1]:
        if 'source_file' in df.columns and not df.empty:    
            file = df['source_file'].iloc[0]
            file_path = os.path.join(csv_directory, file)
            df = df.drop(columns=['source_file'])
            df.to_csv(file_path, index=False)


def remove_rogue_links(df, date):
    date_str = date.strftime('%Y%m%d')
    df = df[df['link'].str.contains(f'/web/{date_str}')]
    return df

# MAIN CODE
def main(burl, corpus_dir, file_name):
    base_url = burl
    csv_directory = corpus_dir
    csv_file_path = os.path.join(csv_directory, f"{file_name}.csv")

    failed_urls = []
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # List of additional fields
    fields = [
        'andhra-pradesh', 'andhra-pradesh/districts', 'andhra-pradesh/districts/alluri-sitharama-raju', 
        'andhra-pradesh/districts/amaravati-krishna', 'andhra-pradesh/districts/anantapur', 
        'andhra-pradesh/districts/chittoor', 'andhra-pradesh/districts/east-godavari', 
        'andhra-pradesh/districts/guntur', 'andhra-pradesh/districts/kurnool', 
        'andhra-pradesh/districts/nellore', 'andhra-pradesh/districts/parvatipuram-manyam', 
        'andhra-pradesh/districts/prakasam', 'andhra-pradesh/districts/srikakulam', 
        'andhra-pradesh/districts/visakhapatnam', 'andhra-pradesh/districts/vizianagaram', 
        'andhra-pradesh/districts/west-godavari', 'andhra-pradesh/districts/ysr', 'business', 
        'business/automobile', 'business/banking-loans', 'business/financial-planning', 'business/information', 
        'business/question-and-answers', 'business/tech-and-gadgets', 'crime', 'devotional', 'education', 'editorial', 'kathalu', 'kids-stories', 
        'elections', 'explained', 'general', 'health', 'india', 'latest-news', 'movies',' movies/ott', 'movies/cinema-review', 'movies/interview', 'movies/cinema-special', 'movies/tv', 'movies/flashback', 'movies/new-updates', 
        'nri', 'photos', 'politics', 'recipes', 'real-estate', 'rashi-phalalu', 
        'rashi-phalalu/dhanu-rashi-today', 'rashi-phalalu/kark-rashi-today', 'rashi-phalalu/kumbh-rashi-today', 
        'rashi-phalalu/makar-rashi-today', 'rashi-phalalu/mesh-rashi-today', 'rashi-phalalu/mithun-rashi-today', 
        'rashi-phalalu/meen-rashi-today', 'rashi-phalalu/singh-rashi-today', 'rashi-phalalu/tula-rashi-today', 
        'rashi-phalalu/vrushabha-rashi-today', 'rashi-phalalu/vrushchik-rashi-today', 'recipes', 'sunday-magazine', 
        'sports', 'technology', 'technology/stories', 'technology/gadgets', 'technology/apps-games', 'technology/science', 'technology/social-media', 'telangana', 'telangana/districts', 'telangana/districts/hyderabad', 'telangana/districts/warangal',
        'telangana/districts/karimnagar', 'telangana/districts/nalgonda', 'telangana/districts/khammam', 'telangana/districts/nizamabad', 'telangana/districts/mahbubnagar', 'telangana/districts/medak', 
        'telangana/districts/adilabad', 'temples', 'trending-news', 
        'videos', 'viral-videos', 'women', 'women/beauty-fashion', 'women/health', 'women/family-relationships', 'women/youth-corner', 'women/sweet-home', 'women/work-life-balance', 'women/empowerment', 'women/expert-opinion', 'world'
    ]

    html_content = fetch_html(base_url)
    if html_content:

        links = extract_links(html_content)

        # Write links to CSV file
        if not is_url_present(csv_file_path, base_url):
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['link']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for link in links:
                    if not is_url_present(csv_file_path, link):
                        writer.writerow({'link': link})
            print(f"Links saved to {file_name}.csv")
        else:
            print("Base URL already exists in the CSV file.")

    else:
        print("Failed to fetch HTML content.")
        random_delay(50, 60)
        failed_urls.append(base_url)

    # Scrape data from each section
    counter = 0
    for field in fields:
        counter += 1
        # Delay after every 15 sections
        if counter % 20 == 0:
            random_delay(50, 60)
            counter = 0  # Reset counter

        new_url = scrape_section(base_url, field)
    
        new_html_content = fetch_html(new_url)
        if new_html_content:
    
            links = extract_links(new_html_content)

            # Write links to CSV file
            if not is_url_present(csv_file_path, new_url):
                with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['link']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for link in links:
                        if not is_url_present(csv_file_path, link):
                            writer.writerow({'link': link})
                print(f"Links saved to {file_name}.csv")
            else:
                print(f"URL {new_url} already exists in the CSV file.")
        else:
            print("Failed to fetch HTML content.")
            if len(failed_urls) < 15:
                random_delay(50, 60)
            failed_urls.append(new_url)

    still_failed = []

    print("----------------------------------------")
    print("Retrying Failed urls")
    print("----------------------------------------")
    for url in failed_urls:
        html_content = fetch_html(url)
        if html_content:

            links = extract_links(html_content)

            # Write links to CSV file
            if not is_url_present(csv_file_path, url):
                with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['link']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for link in links:
                        if not is_url_present(csv_file_path, link):
                            writer.writerow({'link': link})
                print(f"Links saved to {file_name}.csv")
            else:
                print("Base URL already exists in the CSV file.")

        else:
            print("Failed to fetch HTML content.")
            if len(failed_urls) < 20:
                random_delay(50, 60)
            still_failed.append(url)

    failed_csv_path = "/home/llmtelugu/data/wayback_data/Debug/csvfail/still_failed_urls.csv"

    if still_failed:
        print("----------------------------------------")
        print(f"Saving still Failed urls to {failed_csv_path}")
        print("----------------------------------------")
        if not os.path.isfile(failed_csv_path):
            with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
                fieldnames = ['failed_url']
                writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
                writer.writeheader()

        with open(failed_csv_path, 'a', newline='', encoding='utf-8') as failed_csv:
            fieldnames = ['failed_url']
            writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)

            failed_csv.seek(0, os.SEEK_END)
            if failed_csv.tell() == 0:
                writer.writeheader()

            for url in still_failed:
                writer.writerow({'failed_url': url})
        print("Still failed URLs appended to:", failed_csv_path)

        fdf = pd.read_csv(csv_file_path)

        fdf.drop_duplicates(inplace=True)

        fdf.to_csv(csv_file_path, index=False)

        print("Duplicate rows removed from still_failed_urls.csv")
    else:
        print("No URLs failed again.")
        
    df = pd.read_csv(csv_file_path)
    df.drop_duplicates(inplace=True)
    df = remove_overlapping_links(df)
    date_str = file_name[:8]  
    df = remove_rogue_links(df, pd.to_datetime(date_str, format='%Y%m%d'))
    df.to_csv(csv_file_path, index=False)
    clean_csv_directory(csv_directory)
    print(f"Cleaned data written to {file_name} csv")