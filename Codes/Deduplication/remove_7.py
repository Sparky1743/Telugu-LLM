import os
import pandas as pd
import shutil
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import time

output_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/output2"
# target_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_dedup"
# original_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_new"
removed_files_path = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/Logs/removed_files.txt"

def get_nproc():
    try:
        return int(os.popen('nproc').read().strip())
    except Exception as e:
        print(f"Error getting nproc: {e}")
        return None

def effective_cpu_count():
    nproc_count = get_nproc()
    cpu_count_value = cpu_count()

    if nproc_count is not None:
        effective_cpu_count = min(nproc_count, cpu_count_value)
    else:
        effective_cpu_count = cpu_count_value
    return effective_cpu_count

def is_valid_hash(h):
    """Check if the given hash is a valid integer."""
    try:
        int(h)
        return True
    except ValueError:
        return False

def process_row(row, remaining_files, removed_files):
    """Process each row to determine if files should be kept or removed."""
    file1 = row['file1']
    file2 = row['file2']
    similarity = row['similarity']

    if file1 not in remaining_files and file1 not in removed_files:
        remaining_files.add(file1)

    if similarity > 0.8:
        if file2 not in removed_files and file2 not in remaining_files:
            removed_files.add(file2)
    #         if file2 in remaining_files:
    #             remaining_files.remove(file2)
    # else:
    #     if file2 not in remaining_files and file2 not in removed_files:
    #         remaining_files.add(file2)

# def copy_file(file):
#     """Copy a file to the target directory while preserving the relative path."""
#     try:
#         relative_path = os.path.relpath(file, original_dir)
#         target_path = os.path.join(target_dir, relative_path)
#         os.makedirs(os.path.dirname(target_path), exist_ok=True)
#         shutil.copy(file, target_path)
#         return f"Copied {file} to {target_path}"
#     except Exception as e:
#         return f"Error copying {file} to {target_path}: {str(e)}"

def process_csv(csv_file_path, remaining_files, removed_files):
    """Process the CSV file to determine remaining and removed files."""
    df = pd.read_csv(csv_file_path)
    print("Read ", csv_file_path)
    rows = [row for _, row in df.iterrows()]

    for row in tqdm(rows, desc=f"Processing {os.path.basename(csv_file_path)}"):
        process_row(row, remaining_files, removed_files)

def main():
    start = time.time()
    # os.makedirs(target_dir, exist_ok=True)

    # Get list of CSV files in the output directory
    csv_files = [os.path.join(output_dir, file_name) for file_name in os.listdir(output_dir) if file_name.endswith('.csv')]
    print(f"Total number of CSV files: {len(csv_files)}")
    
    remaining_files = set()
    removed_files = set()
    
    # Process each CSV file
    for csv_file in tqdm(csv_files, desc = "Processing csvs"):
        process_csv(csv_file, remaining_files, removed_files)

    # Remove any file from remaining_files that is also in removed_files
    final_remaining_files = remaining_files - removed_files

    print(f"Total number of remaining files: {len(final_remaining_files)}")
    print(f"Total number of removed files: {len(removed_files)}")
    print(f"Total files: {len(final_remaining_files) + len(removed_files)}")
    
    # Save the removed files to a disk
    with open(removed_files_path, 'w') as f:
        for file in removed_files:
            f.write(f"{file}\n")

    print(f"Removed files saved to {removed_files_path}")

    # # Copy remaining files to target directory in parallel
    # with Pool(processes=effective_cpu_count()) as pool:
    #     for _ in tqdm(pool.imap(copy_file, final_remaining_files), total=len(final_remaining_files), desc="Copying remaining files"):
    #         pass

    print("Total time:", time.time() - start)

if __name__ == "__main__":
    main()
