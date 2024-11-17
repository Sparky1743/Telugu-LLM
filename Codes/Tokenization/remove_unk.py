import os
import pandas as pd
import ast
from tqdm import tqdm

def process_tokens(tokens):
    """
    Removes the number 5 from a list of tokens.
    """
    return [token for token in tokens if token != 5]

def process_csv_files(input_folder, output_folder, log_file):
    """
    Processes all CSV files in the given folder and its subfolders.
    Removes the number 5 from the 'tokens' column in each file.
    Saves the modified CSVs in the output folder while maintaining the relative structure.
    Logs the number of rows processed for each file.
    """
    with open(log_file, 'w') as log:
        log.write("Log File for Token Removal\n")
        log.write("=" * 40 + "\n")
        log.flush()  
        
        for root, _, files in os.walk(input_folder):
            for file in tqdm([f for f in files if f.endswith('.csv')], desc="Processing CSV files"):
                file_path = os.path.join(root, file)
                
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_file_path = os.path.join(output_dir, file)

                try:
                    df = pd.read_csv(file_path)

                except Exception as e:
                    log.write(f"Error reading {file_path}: {e}\n")
                    log.flush()
                    continue
                
                if 'tokens' in df.columns:
                    try:
                        rows_with_5 = df['tokens'].apply(lambda x: 5 in ast.literal_eval(x)).sum()
                        
                        if rows_with_5 > 0:
                            log.write(f"{file} has {rows_with_5} rows containing the number 5.\n")
                            log.flush()

                        df['tokens'] = df['tokens'].apply(lambda x: process_tokens(ast.literal_eval(x)))
                        
                        df.to_csv(output_file_path, index=False)

                    except Exception as e:
                        log.write(f"Error processing tokens in {file_path}: {e}\n")
                        log.flush()
                        continue
                else:
                    log.write(f"{file_path}: 'tokens' column not found.\n")
                    log.flush()

        log.write("=" * 40 + "\n")
        log.write("Processing completed.\n")
        log.flush()

input_folder = "/raid/telugu_llm/rewriting_reality/telugu/Tokenized_data_eos_with_unk"
output_folder = "/raid/telugu_llm/rewriting_reality/telugu/Tokenized_data_eos_without_unk"
log_file = "/raid/telugu_llm/rewriting_reality/telugu/Tokenized_data_eos_without_unk/Logs/corss_check.txt"

process_csv_files(input_folder, output_folder, log_file)
