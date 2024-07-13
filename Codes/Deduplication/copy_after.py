import os
import shutil
import pandas as pd
import concurrent.futures
from tqdm import tqdm

# Define the directories
csv_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/after"
target_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_dedup"
original_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_new"

def copy_file(file):
    """Copy a file to the target directory while preserving the relative path."""
    try:
        relative_path = os.path.relpath(file, original_dir)
        target_path = os.path.join(target_dir, relative_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy(file, target_path)
        return f"Copied {file} to {target_path}"
    except Exception as e:
        return f"Error copying {file} to {target_path}: {str(e)}"

def process_csv(csv_file):
    """Process a single CSV file."""
    csv_path = os.path.join(csv_folder, csv_file)
    try:
        df = pd.read_csv(csv_path)
        if 'file' in df.columns:
            file_paths = df['file'].tolist()
            return file_paths
        else:
            print(f"CSV {csv_file} does not contain 'file' column.")
            return []
    except Exception as e:
        print(f"Error processing {csv_file}: {str(e)}")
        return []

def main():
    all_files = []

    # Gather all file paths from the CSV files using multiprocessing
    csv_files = [csv_file for csv_file in os.listdir(csv_folder) if csv_file.endswith('.csv')]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_csv, csv_files), total=len(csv_files), desc="Loading CSVs"))

    for file_list in results:
        all_files.extend(file_list)

    # Use ThreadPoolExecutor to copy files in parallel
    futures = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for file_path in tqdm(all_files, desc="Submitting copy tasks"):
            if os.path.exists(os.path.join(original_dir, file_path)):
                future = executor.submit(copy_file, os.path.join(original_dir, file_path))
                futures[future] = file_path

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Copying files"):
            print(future.result())

# Run the script
if __name__ == "__main__":
    main()
