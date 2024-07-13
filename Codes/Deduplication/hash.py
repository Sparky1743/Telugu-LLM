import os
import re
from simhash import Simhash 
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def compute_simhash(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    simhash_value = Simhash(get_features(content))
    return file_path, simhash_value.value


def process_directory(args):
    path, parent = args
    data = []
    relative_path = os.path.relpath(path, parent)

    # Skip processing if the output CSV already exists
    if os.path.exists(output_file):
        print(f"Skipping {path}, CSV already exists")
        return data

    s = relative_path.replace(os.sep, '_')
    for file in tqdm(os.listdir(path), leave=False, desc=s):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_path, simhash_value = compute_simhash(file_path)
            data.append({
                "file": file_path,
                "hash": simhash_value
            })
    if data:
        df = pd.DataFrame(data)
        df.to_csv(f"/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/before/{s}.csv", index=False)
    return data


if __name__ == '__main__':
    parent = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_new"
    directories = [(os.path.join(path, d), parent) for path, dirs, files in os.walk(parent) for d in dirs]

    # Use all available CPUs (one cpu per csv)
    with Pool(cpu_count()) as pool:
        pool.map(process_directory, directories)
