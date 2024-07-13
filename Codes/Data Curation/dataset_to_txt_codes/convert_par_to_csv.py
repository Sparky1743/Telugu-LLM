import os
import pandas as pd
import re

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.parquet'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = file_name.replace('.parquet', '.csv')
            output_file_path = os.path.join(output_dir, output_file_name)

            df = pd.read_parquet(input_file_path)

            # Write to CSV with UTF-8 encoding
            df.to_csv(output_file_path, index=False, encoding='utf-8')

            print(f"Converted {input_file_path} to {output_file_path}")