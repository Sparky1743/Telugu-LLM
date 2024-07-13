# import os
# import pandas as pd
# import tqdm

# def get_ids_to_delete(input_file_path):
#     df = pd.read_csv(input_file_path)
#     # Subtract 1 from each id to adjust for zero-based indexing
#     return [id - 1 for id in df['id'].tolist()]

# def delete_rows(data_file_path, ids_to_delete):
#     df = pd.read_csv(data_file_path)
#     df = df[~df.index.isin(ids_to_delete)]
#     df.reset_index(drop=True, inplace=True)
#     return df

# def process_all_files(input_folder, data_folder, output_folder):
#     for root, _, files in os.walk(input_folder):
#         for file in tqdm.tqdm(files, desc="Processing input files"):
#             if file.endswith('.csv'):
#                 input_file_path = os.path.join(root, file)
#                 data_file_path = os.path.join(data_folder, file)
#                 output_file_path = os.path.join(output_folder, file)
                
#                 if os.path.exists(data_file_path):
#                     ids_to_delete = get_ids_to_delete(input_file_path)
#                     modified_df = delete_rows(data_file_path, ids_to_delete)
                    
#                     # Ensure the output directory exists
#                     os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    
#                     # Save the modified DataFrame to the output file
#                     modified_df.to_csv(output_file_path, index=False)
#                 else:
#                     print(f"Data file {data_file_path} not found.")

# input_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro2"
# data_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/all_webs_data"
# output_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/all_webs_data_including_dates"

# process_all_files(input_folder, data_folder, output_folder)

# print("Processing complete. Specified rows deleted and saved to the output folder.")    

import os
import pandas as pd
import tqdm

def get_ids_to_delete(input_file_path):
    df = pd.read_csv(input_file_path)
    return [id - 1 for id in df['id'].tolist()] # substracting 1 because adding 1 to index in info_iden_csv.py

def delete_rows(data_file_path, ids_to_delete):
    df = pd.read_csv(data_file_path)
    deleted_rows = df[df.index.isin(ids_to_delete)]
    df = df[~df.index.isin(ids_to_delete)]
    df.reset_index(drop=True, inplace=True)
    deleted_rows.reset_index(drop=True, inplace=True)
    return df, deleted_rows

def process_all_files(input_folder, data_folder, output_folder, deleted_folder):
    for root, _, files in os.walk(input_folder):
        for file in tqdm.tqdm(files, desc="Processing input files"):
            if file.endswith('.csv'):
                input_file_path = os.path.join(root, file)
                data_file_path = os.path.join(data_folder, file)
                output_file_path = os.path.join(output_folder, file)
                deleted_file_path = os.path.join(deleted_folder, file)
                
                if os.path.exists(data_file_path):
                    ids_to_delete = get_ids_to_delete(input_file_path)
                    modified_df, deleted_rows_df = delete_rows(data_file_path, ids_to_delete)

                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    os.makedirs(os.path.dirname(deleted_file_path), exist_ok=True)

                    modified_df.to_csv(output_file_path, index=False)
                    deleted_rows_df.to_csv(deleted_file_path, index=False)
                else:
                    print(f"Data file {data_file_path} not found.")

input_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro_2/CSV"
data_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV"
output_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV_dates_remaining"
deleted_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV_dates_removed"

process_all_files(input_folder, data_folder, output_folder, deleted_folder)

print("Processing complete. Specified rows deleted and saved to the output folder.")
