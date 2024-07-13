import pandas as pd
import re
import os
import tqdm

def is_english_word(word):
    return re.match(r'[a-zA-Z]+$', word) is not None

def process_csv_files(input_folder, output_folder_with_english, output_folder_without_english, log_folder_without_english, log_folder_with_english):
    # Ensure output directories exist
    os.makedirs(output_folder_with_english, exist_ok=True)
    os.makedirs(output_folder_without_english, exist_ok=True)
    os.makedirs(log_folder_without_english, exist_ok=True)
    os.makedirs(log_folder_with_english, exist_ok=True)


    # Iterate over all CSV files in the input folder
    for filename in tqdm.tqdm(os.listdir(input_folder), desc="Processing CSVs"):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)

            # Lists to hold rows with and without more than 7 English words
            rows_with_english_words = []
            rows_without_english_words = []
            log_entries_without_english_words = []
            log_entries_with_english_words = []

            # Iterate through each row in the dataframe
            for index, row in df.iterrows():
                # Split the content into words
                words = row['content'].split()
                # Count the number of English words
                english_words = [word for word in words if is_english_word(word)]
                english_words_count = len(english_words)
                # If the count of English words is greater than 7, add to the appropriate list
                if english_words_count > 7:
                    rows_with_english_words.append(row)
                    log_entries_with_english_words.append(f"Row {index}: {english_words}")
                else:
                    rows_without_english_words.append(row)
                    log_entries_without_english_words.append(f"Row {index}: {english_words}")

            # Convert lists to dataframes
            df_with_english_words = pd.DataFrame(rows_with_english_words)
            df_without_english_words = pd.DataFrame(rows_without_english_words)

            # Write the rows with more than 7 English words to a new CSV file
            output_file_with_english = os.path.join(output_folder_with_english, f"with_english_{filename}")
            df_with_english_words.to_csv(output_file_with_english, index=False, encoding='utf-8')

            # Write the remaining rows to another CSV file
            output_file_without_english = os.path.join(output_folder_without_english, f"{filename}")
            df_without_english_words.to_csv(output_file_without_english, index=False, encoding='utf-8')

            # Write the log file for rows with fewer than 7 English words
            log_file_path_without_english = os.path.join(log_folder_without_english, f"log_{filename.replace('.csv', '.txt')}")
            with open(log_file_path_without_english, 'w', encoding='utf-8') as log_file:
                for entry in log_entries_without_english_words:
                    log_file.write(f"{entry}\n")

            # Write the log file for rows with more than 7 English words
            log_file_path_with_english = os.path.join(log_folder_with_english, f"log_{filename.replace('.csv', '.txt')}")
            with open(log_file_path_with_english, 'w', encoding='utf-8') as log_file:
                for entry in log_entries_with_english_words:
                    log_file.write(f"{entry}\n")

            print(f"Finished processing {filename}")

# Define the input folder and output folders
input_folder = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test_pro/input'
output_folder_with_english = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test_pro/with_eng'
output_folder_without_english = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test_pro/without_eng'
log_folder_without_english = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test_pro/logs_without_eng'
log_folder_with_english = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test_pro/logs_with_eng'


# Process the CSV files
process_csv_files(input_folder, output_folder_with_english, output_folder_without_english, log_folder_without_english, log_folder_with_english)
