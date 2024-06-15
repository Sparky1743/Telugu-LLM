import os
import pandas as pd
from datetime import datetime, timedelta

directory = '/home/llmtelugu/data/sakshi_data/oldcsv'

existing_dates = set()

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        try:
            date_str = filename[:-4]  # Remove the '.csv' extension
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            existing_dates.add(date_obj)
        except ValueError:
            continue

start_date = datetime.strptime('2022-01-01', '%Y-%m-%d').date()
end_date = datetime.strptime('2024-05-19', '%Y-%m-%d').date()

all_dates = set()
current_date = start_date
while current_date <= end_date:
    all_dates.add(current_date)
    current_date += timedelta(days=1)

missing_dates = all_dates - existing_dates

print("Missing Dates:")
for date in sorted(missing_dates):
    print(date)

missing_dates_df = pd.DataFrame(sorted(missing_dates), columns=['Missing Dates'])
missing_dates_df.to_csv('/home/llmtelugu/data/sakshi_data/Debug/missing/missing_dates.csv', index=False)
