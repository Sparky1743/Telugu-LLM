import os
import pandas as pd
from tqdm import tqdm

path = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/before"
output_path = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/after"
log_file_path = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/Logs/duprows_log.txt"

files = list(os.listdir(path))
files.sort()
print("Number of files:", len(files), files)
files = [f"{path}/{x}" for x in files]

with open(log_file_path, 'a') as log_file:
    for file in tqdm(files):
        print(file)
        df = pd.read_csv(file)
        
        # Identify duplicates
        duplicates = df[df.duplicated(subset='hash', keep=False)]
        
        if not duplicates.empty:
            log_file.write(f"Duplicates in {file}:\n")
            for index, row in duplicates.iterrows():
                log_file.write(f"\tFile: {row['file']} Hash: {row['hash']}\n")
            log_file.write("\n")
        
        # Remove duplicates
        df = df.drop_duplicates(subset='hash', keep="first")

        s = file.split("/")[-1]
        print(s)
        df.to_csv(f"{output_path}/{s}", index=False)
        print("Deduplication done for", file)

print(f"Duplicate log has been saved to {log_file_path}")
