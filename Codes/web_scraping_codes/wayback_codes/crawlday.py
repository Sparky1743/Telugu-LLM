import csv
import createcsv
import smartial
import os
from datetime import datetime

date1 = "2022-01-01" 
date2 = "2022-03-31"

def process_snapshots(snapshot_csv_path, csv_directory):
    # Read the CSV file and convert it to a dictionary
    snapshot_dict = {}
    with open(snapshot_csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['Date']
            snapshots = [row['Latest Snapshot']]
            snapshot_dict[date] = [snap for snap in snapshots if snap]

    # Process each date and its snapshots
    for date, snapshots in snapshot_dict.items():
        file_name = date
        for snapshot in snapshots:
            base_url = f"https://web.archive.org/web/{snapshot}/https://www.eenadu.net/"
            createcsv.main(base_url, csv_directory, file_name)

        print("----------------------------------------")
        print("Running text extraction")
        print("----------------------------------------")

        smartial.main(os.path.join(csv_directory, f"{file_name}.csv"), f"/home/llmtelugu/data/wayback_data/eenadu/text_data/{file_name}.txt")

        # Logging the completion of processing
        log_file_path = os.path.join("/home/llmtelugu/data/wayback_data/Debug/Logs", "log.txt")
        with open(log_file_path, 'a', newline='', encoding='utf-8') as log_file:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{file_name}.txt is done on {current_time}\n")
        print(f"Logged completion of {file_name}.txt processing")

# Example usage
print("---------------------------------------------------------------")
print(f"crawling {date1} to {date2}")
print("---------------------------------------------------------------")
snapshot_csv_path = f"/home/llmtelugu/data/wayback_data/eenadu/eenaducsv/snapshots/eenadu_snapshots_{date1}_{date2}.csv"
csv_directory = "/home/llmtelugu/data/wayback_data/eenadu/eenaducsv/created_csvs"

process_snapshots(snapshot_csv_path, csv_directory)
