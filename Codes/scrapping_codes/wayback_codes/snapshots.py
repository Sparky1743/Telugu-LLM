import csv
import requests
from datetime import datetime
# import random

def get_latest_and_random_snapshots(domain, start_date, end_date):
    snapshot_dict = {}
    start_year = start_date.year
    end_year = end_date.year
    cdx_url = f"https://web.archive.org/cdx/search/cdx?url={domain}&from={start_year}&to={end_year}&output=json"
    response = requests.get(cdx_url)
    
    if response.status_code == 200:
        snapshots = response.json()
        
        for snapshot in snapshots[1:]:
            timestamp = snapshot[1][:8]  # Extracting the YYYYMMDD part of the timestamp
            snapshot_date = datetime.strptime(timestamp, "%Y%m%d").date()
            if start_date <= snapshot_date <= end_date:
                if timestamp not in snapshot_dict:
                    snapshot_dict[timestamp] = []
                
                snapshot_dict[timestamp].append(snapshot[1])
        
        # Get the latest snapshot and any random snapshot for each day
        for date, snapshot_list in snapshot_dict.items():
            latest_snapshot = snapshot_list[-1]
            # random_snapshot = random.choice(snapshot_list[:-1]) if len(snapshot_list) > 1 else None
            snapshot_dict[date] = [latest_snapshot]
            
        return snapshot_dict
    else:
        print("Failed to fetch snapshots.")
        return None

def save_snapshots_to_csv(snapshot_dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Latest Snapshot'])
        for date, snapshots in snapshot_dict.items():
            row = [date] + snapshots
            writer.writerow(row)

# Example usage
domain = "www.eenadu.net"
start_date = datetime(2022, 1, 1).date()  # Example start date: January 1, 2024
end_date = datetime(2022, 3, 31).date()  # Example end date: December 31, 2024
output_path = f"/home/llmtelugu/data/wayback_data/eenadu/eenaducsv/snapshots/eenadu_snapshots_{start_date}_{end_date}.csv"
snapshots = get_latest_and_random_snapshots(domain, start_date, end_date)

if snapshots:
    save_snapshots_to_csv(snapshots, output_path)
    print(f"Snapshots from {start_date} - {end_date} saved to {output_path}")
else:
    print("No snapshots found.")
