import os
import re
import json
import pandas as pd
import tqdm

# Load unwanted words from the JSON file
with open('build.json') as unwanted_word_file:
    unwanted_data = json.load(unwanted_word_file)

# Define regex patterns
email_pattern = r"\S+@\S+"
phone_pattern = r'[\+\(]?[0-9][0-9 .\-\(\)]{5,}[0-9]'
correct_phone_pattern = r"[\s\(]?(\d{4}\s*-\s*\d{4}|\d{2}\s*[.-]\s*\d{2}\s*[.-]\s*\d{4}|\d{4}\s*[.-]\s*\d{2}\s*[.-]\s*\d{2})\s?$"
unwanted_words = "|".join(unwanted_data["te"])

def extracted_text(text):
    matches = re.findall(f"(?:{email_pattern}|{phone_pattern}|{unwanted_words})", text)
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

def process_csv_file(input_file_path, output_file_path):
    df = pd.read_csv(input_file_path)

    all_matches = []
    for index in range(len(df)):
        matches = extracted_text(df.iloc[index, 1])
        if matches:
            all_matches.append({
                'id': df.iloc[index, 0],  # Assuming the first column is 'id'
                'list': ', '.join(matches)
            })

    matches_df = pd.DataFrame(all_matches, columns=['id', 'list'])

    # Write matches to a CSV file
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    matches_df.to_csv(output_file_path, index=False, header=True)

def process_all_csv_files(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for file in tqdm.tqdm(files, desc="Processing"):
            if file.endswith('.csv'):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_folder)
                output_file_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.csv')
                process_csv_file(input_file_path, output_file_path)

input_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro/CSV"
output_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro_2/CSV"

process_all_csv_files(input_folder, output_folder)

print("Processing complete. All matches written to CSV files.")


# for datasets slightly different variation

# import os
# import re
# import json
# import pandas as pd
# from tqdm import tqdm
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Load unwanted words from the JSON file
# with open('build.json') as unwanted_word_file:
#     unwanted_data = json.load(unwanted_word_file)

# # Define regex patterns
# email_pattern = r"\S+@\S+"
# phone_pattern = r'[\+\(]?[0-9][0-9 .\-\(\)]{5,}[0-9]'
# date_pattern = r"[\s\(]?(\d{4}\s*-\s*\d{4}|\d{2}\s*[.-]\s*\d{2}\s*[.-]\s*\d{4}|\d{4}\s*[.-]\s*\d{2}\s*[.-]\s*\d{2})\s?$"
# unwanted_words = "|".join(unwanted_data["te"])

# def contains_only_date(text):
#     # Check if the text contains a date
#     date_match = re.search(date_pattern, text)
#     if not date_match:
#         return False
    
#     # Check if the text contains any unwanted patterns
#     if re.search(email_pattern, text) or re.search(phone_pattern, text) or re.search(unwanted_words, text):
#         return False
    
#     return True

# def process_csv_file(input_file_path, output_file_path):
#     df = pd.read_csv(input_file_path)
#     logging.info(f"Processing file: {input_file_path}")
#     logging.info(f"Total rows in input: {len(df)}")

#     filtered_rows = []
#     for _, row in df.iterrows():
#         content = str(row.iloc[1])
#         if contains_only_date(content):
#             filtered_rows.append({
#                 'id': row.iloc[0],
#                 'content': content
#             })
#         elif re.search(date_pattern, content):
#             # Fallback: include rows with dates even if they have other content
#             filtered_rows.append({
#                 'id': row.iloc[0],
#                 'content': content
#             })

#     filtered_df = pd.DataFrame(filtered_rows, columns=['id', 'content'])
#     logging.info(f"Filtered rows: {len(filtered_df)}")

#     # Write filtered rows to a CSV file
#     os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
#     filtered_df.to_csv(output_file_path, index=False, header=True)
#     logging.info(f"Output written to: {output_file_path}")

# def process_all_csv_files(input_folder, output_folder):
#     for root, _, files in os.walk(input_folder):
#         for file in tqdm(files, desc="Processing"):
#             if file.endswith('.csv'):
#                 input_file_path = os.path.join(root, file)
#                 relative_path = os.path.relpath(input_file_path, input_folder)
#                 output_file_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.csv')
#                 process_csv_file(input_file_path, output_file_path)

# input_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro/datasets_new"
# output_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro_2/datasets"

# process_all_csv_files(input_folder, output_folder)

# print("Processing complete. Filtered rows written to CSV files.")