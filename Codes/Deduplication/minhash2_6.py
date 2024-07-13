import os
import re
import pandas as pd
from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
import pickle
from multiprocessing import Pool, cpu_count
import time

def get_features(s):
    """Generate features from a string."""
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return set(s[i:i + width] for i in range(max(len(s) - width + 1, 1)))

def is_valid_hash(h):
    """Check if the given hash is a valid integer."""
    try:
        int(h)
        return True
    except ValueError:
        return False

def process_csv_file(args):
    """Process each CSV file to extract MinHash objects."""
    input_dir, file_name = args
    file_path = os.path.join(input_dir, file_name)
    df = pd.read_csv(file_path)
    file_minhashes = []
    # print(df.iterrows())
    for index, row in df.iterrows():
        file_minhashes.append((str(row['file']),str(row['hash'])))

    return file_minhashes

def generate_minhash(file_data):
    """Generate MinHash for each file."""
    print(file_data)
    file, features = file_data
    minhash = MinHash(num_perm=128)
    for feature in features:
        minhash.update(feature.encode('utf8'))
    return file, minhash

def query_minhash(args):
    """Query the LSH for near-duplicates for a given file and its MinHash."""
    index, file_minhash_pairs, output_file_path, minhash_lsh, file_minhash_map, no_of_files = args
    data = []
    iteration_index = 0
    for file, minhash in file_minhash_pairs:
        result = minhash_lsh.query(minhash)
        for other_file in result:
            if file != other_file:  # Ensure we don't compare a file with itself
                similarity = minhash.jaccard(file_minhash_map[other_file])
                data.append({
                    'file1': file,
                    'hash1': str(minhash),
                    'file2': other_file,
                    'hash2': str(file_minhash_map[other_file]),
                    'similarity': similarity
                })
                iteration_index += 1
                if len(data) >= no_of_files:
                    save_chunk(data, output_file_path, index, iteration_index)
                    data.clear()  # Clear the data list to free memory

    # Save any remaining data to a CSV chunk
    if data:
        save_chunk(data, output_file_path, index, iteration_index)
        data.clear()  # Clear the data list to free memory

    return f"Chunk {index} processed"

def save_chunk(data, output_file_path, index, iteration_index):
    """Save a chunk of data to a CSV file."""
    df = pd.DataFrame(data)
    chunk_output_path = os.path.join(output_file_path, f"chunk_{index}_{iteration_index}.csv")
    df.to_csv(chunk_output_path, index=False)
    print(f"Saved chunk {index} to {chunk_output_path}")

def main(store_model=False):
    start = time.time()
    input_dir = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test/before'
    output_file_path = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test/after'
    cache_dir = '/nlsasfs/home/aipsc/myksingh/llmtelugu/test/cache'
    os.makedirs(output_file_path, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)
    no_of_files = 30000000  # Number of files per chunk
    
    
    # Stage 1: Process CSV files and store results in data.pkl
    file_minhash_map_path = os.path.join(cache_dir, 'file_minhash_map.pkl')
    if not os.path.exists(file_minhash_map_path):
        data_pkl_path = os.path.join(cache_dir, 'data.pkl')
        if not os.path.exists(data_pkl_path):
            csv_files = [(input_dir, file_name) for file_name in os.listdir(input_dir)]
            with Pool(cpu_count()) as pool:
                all_files = list(tqdm(pool.imap(process_csv_file, csv_files), total=len(csv_files), desc="Processing CSV files"))
            
            all_files = [item for sublist in all_files for item in sublist]

            with open(data_pkl_path, 'wb') as f:
                pickle.dump(all_files, f)
        else:
            with open(data_pkl_path, 'rb') as f:
                all_files = pickle.load(f)
        print("Loaded data.pkl")

        # Stage 2: Generate MinHash objects and store results in file_minhash_map.pkl
        with Pool(cpu_count()) as pool:
            minhash_results = list(tqdm(pool.imap(generate_minhash, all_files), total=len(all_files), desc="Generating MinHash objects"))
        file_minhash_map = dict(minhash_results)
        with open(file_minhash_map_path, 'wb') as f:
            pickle.dump(file_minhash_map, f)
    else:
        with open(file_minhash_map_path, 'rb') as f:
            file_minhash_map = pickle.load(f)
    print("Loaded file_minhash_map.pkl")

    # Stage 3: Load MinHashLSH and insert MinHash objects
    minhash_lsh_path = os.path.join(cache_dir, 'minhash_lsh.pkl')
    if not os.path.exists(minhash_lsh_path):
        minhash_lsh = MinHashLSH(threshold=0.5, num_perm=128)
        for file, minhash in tqdm(file_minhash_map.items(), desc="Inserting data in model"):
            minhash_lsh.insert(file, minhash)
        if store_model:
            with open(minhash_lsh_path, 'wb') as f:
                pickle.dump(minhash_lsh, f)
    else:
        with open(minhash_lsh_path, 'rb') as f:
            minhash_lsh = pickle.load(f)
    print("Loaded minhash_lsh.pkl")

    # Stage 4: Query MinHashLSH and save results in chunks
    file_minhash_pairs = list(file_minhash_map.items())
    num_processes = cpu_count()
    chunk_size = len(file_minhash_pairs) // num_processes
    if chunk_size == 0:
        chunk_size = 1
    chunks = [file_minhash_pairs[i:i + chunk_size] for i in range(0, len(file_minhash_pairs), chunk_size)]
    
    if len(chunks) > num_processes:
        chunks[-2].extend(chunks[-1])
        chunks.pop()

    args_list = [(index, chunk, output_file_path, minhash_lsh, file_minhash_map, no_of_files) for index, chunk in enumerate(chunks)]

    # Use multiprocessing to query MinHashLSH
    with Pool(processes=num_processes) as pool:
        results = list(tqdm(pool.imap(query_minhash, args_list), total=len(args_list), desc="Querying MinHashLSH"))

    print(f"Done, results saved to {output_file_path}")
    print("Time Taken", time.time() - start)

if __name__ == "__main__":
    store_model = False  # Change to True if you want to store the model
    main(store_model)
