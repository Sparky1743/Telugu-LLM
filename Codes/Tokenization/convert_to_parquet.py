import pandas as pd
import ast
from datasets import Dataset
import os

input_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokens_2048/"
output_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/2_test/"

csv_files = [f"processed_tokens_{i}.csv" for i in range(70, 79)]  

print("started")
for file_name in csv_files:
    df = pd.read_csv(os.path.join(input_folder, file_name))

    df["input_ids"] = df.iloc[:, 0].apply(lambda x: ast.literal_eval(x))

    df = df[["input_ids"]]

    hf_dataset = Dataset.from_pandas(df)

    parquet_file_path = os.path.join(output_folder, f"{file_name.replace('.csv', '.parquet')}")

    hf_dataset.to_parquet(parquet_file_path)

print("Individual Parquet files saved in:", output_folder)
