import csv
import json
import re
import os

# Compile the regex pattern to match specific bad words
pattern = re.compile(r'\b\S*(fuck|shit|lesbian|bitch|sex|porn)\S*\b', re.IGNORECASE)

input_folder = '/nlsasfs/home/aipsc/myksingh/telugu_llm/English_Vinglish/final/filtered_csvs_2'
output_folder = '/nlsasfs/home/aipsc/myksingh/telugu_llm/English_Vinglish/final/cleaned_csvs'
os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_folder, filename)
        
        with open(input_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

        cleaned_data = []

        for row in rows:
            if any(pattern.search(cell) for cell in row):
                continue  # Skip rows with bad words
            cleaned_data.append(row)  # Keep rows without bad words

        # Write the cleaned data to a new CSV file in the output folder
        output_file_path = os.path.join(output_folder, filename)
        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(cleaned_data)

print("All CSV files have been cleaned and saved to the output folder.")
