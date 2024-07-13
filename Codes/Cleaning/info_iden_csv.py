import os
import re
import json
import pandas as pd
import tqdm

with open('build.json') as unwanted_word_file:
    unwanted_data = json.load(unwanted_word_file)

email_pattern = r"\S+@\S+"
phone_pattern = r'[\+\(]?[0-9][0-9 .\-\(\)]{5,}[0-9]'
correct_phone_pattern = r"\s?\d{4}-\d{4}\s?$"
unwanted_words = "|".join(unwanted_data["te"])

def extracted_text(text):
    matches = re.findall(f"""(?:{email_pattern}|{phone_pattern}|{unwanted_words})""", text)
    filtered_matches = []
    
    for match in matches:
        if re.match(phone_pattern, match):
            if re.match(correct_phone_pattern, match):
                continue  
            digit_count = len(re.sub(r'\D', '', match))
            if digit_count > 7:
                filtered_matches.append(match)
        else:
            filtered_matches.append(match)
    
    return [match for match in filtered_matches if match]

def process_csv_file(input_file_path,output_file_path):
    df = pd.read_csv(input_file_path)

    all_matches = []
    for index in range(len(df)):
        # df.iloc[index,1]
        x = extracted_text(df.iloc[index,1])
        if x:
            all_matches.append({
                'line': index + 1, #dont keep +1, -1 to all values in return_rows
                'matches': ', '.join(x)
            })

    matches_df = pd.DataFrame(all_matches)

    # Write matches to a CSV file
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    matches_df.to_csv(output_file_path, index=False, header=False)


def process_all_csv_files(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for file in tqdm.tqdm(files, desc = "processing"):
            if file.endswith('.csv'):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_folder)
                output_file_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.csv')
                process_csv_file(input_file_path, output_file_path)


input_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV"
output_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro/CSV"

process_all_csv_files(input_folder, output_folder)

print("Processing complete. All matches written to CSV files.") 