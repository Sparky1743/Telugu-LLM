import glob
import os
from datasets import Dataset, concatenate_datasets

input_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/2_test"
output_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/4_test"
output_file_name = "combined_dataset.parquet"

parquet_files = glob.glob(os.path.join(input_folder, "*.parquet"))
parquet_files = sorted(parquet_files, key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))

datasets = [Dataset.from_parquet(file) for file in parquet_files]

combined_dataset = concatenate_datasets(datasets)

output_file_path = os.path.join(output_folder, output_file_name)
combined_dataset.to_parquet(output_file_path)

print("All Parquet files have been merged in integer order and saved as a Hugging Face dataset at:", output_file_path)
