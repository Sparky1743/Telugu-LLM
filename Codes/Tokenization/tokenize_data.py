import os
import pandas as pd
from transformers import AutoTokenizer
import logging
import time

tokenizer = AutoTokenizer.from_pretrained("/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenizer/Tokenizer")

logging.basicConfig(
    filename="/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenized_data/Logs/time_estimation.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def process_file(input_file_path, output_file_path, batch_size=100):
    start_time = time.time()
    chunk_iter = pd.read_csv(input_file_path, chunksize=batch_size)
    processed_chunks = []

    for chunk in chunk_iter:
        if "id" not in chunk.columns or "content" not in chunk.columns:
            logging.error(f"Columns 'id' and 'content' are missing in {input_file_path}")
            raise ValueError(f"Columns 'id' and 'content' are required in {input_file_path}")

        # Check for NaN values
        nan_indices = chunk[chunk['content'].isna()].index.tolist()
        nan_count = len(nan_indices)
        
        if nan_count > 0:
            logging.info(f"Found {nan_count} NaN values in 'content' column in {input_file_path} at rows: {nan_indices}")

        # Replace NaN with an empty string and convert all content to string
        chunk['content'] = chunk['content'].fillna('').astype(str)

        rows = chunk["content"].tolist()
        
        # Debugging: Check for non-string entries
        for i, row in enumerate(rows):
            if not isinstance(row, str):
                logging.error(f"Row {i} is not a string: {row}")

        x = tokenizer(rows, return_token_type_ids=False, return_attention_mask=False)
        
        chunk['tokens'] = x['input_ids']
        
        processed_chunks.append(chunk)

    output_df = pd.concat(processed_chunks, ignore_index=True)
    output_df.to_csv(output_file_path, index=False)
    
    elapsed_time = time.time() - start_time


def process_folder(input_folder, output_folder, batch_size=100):
    total_files = sum(len(files) for _, _, files in os.walk(input_folder) if files)
    processed_files = 0
    start_time = time.time()
    logging.info("Starting folder processing...")

    for root, dirs, files in os.walk(input_folder):
        rel_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, rel_path)

        os.makedirs(output_dir, exist_ok=True)

        csv_files = [f for f in files if f.endswith(".csv")]
        if csv_files:
            logging.info(f"Processing {len(csv_files)} files in folder: {rel_path}")
            
        for filename in csv_files:
            input_file_path = os.path.join(root, filename)
            output_file_path = os.path.join(output_dir, filename)
            process_file(input_file_path, output_file_path, batch_size=batch_size)

            processed_files += 1
            elapsed_time = time.time() - start_time
            avg_time_per_file = elapsed_time / processed_files
            remaining_files = total_files - processed_files
            estimated_time_remaining = avg_time_per_file * remaining_files

            logging.info(
                f"Processed {processed_files}/{total_files} files. "
                f"Estimated time remaining: {estimated_time_remaining / 60:.2f} minutes."
            )

        logging.info(f"Completed processing all files in folder: {rel_path}")
        print(f"Completed processing all files in folder: {rel_path}")

    total_elapsed_time = time.time() - start_time
    logging.info(f"Completed processing all files in {total_elapsed_time / 60:.2f} minutes.")
    print(f"Completed processing all files in {total_elapsed_time / 60:.2f} minutes.")

input_folder = '/nlsasfs/home/aipsc/myksingh/telugu_llm/Tokenizer_input'
output_folder = '/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenized_data'
process_folder(input_folder, output_folder, batch_size=50000)
