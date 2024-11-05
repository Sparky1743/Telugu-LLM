import pandas as pd
import ast
import os

def process_csv_files(input_folder, output_folder):
    for dirpath, _, filenames in os.walk(input_folder):
        for filename in filenames:
            if filename.endswith('.csv'):
                input_file_path = os.path.join(dirpath, filename)

                df = pd.read_csv(input_file_path)

                df['tokens'] = df['tokens'].apply(ast.literal_eval)
                
                df['tokens'] = df['tokens'].apply(lambda x: x + [3])

                output_dir = os.path.join(output_folder, os.path.relpath(dirpath, input_folder))
                os.makedirs(output_dir, exist_ok=True)

                output_file_path = os.path.join(output_dir, filename)
                df.to_csv(output_file_path, index=False)

                print(f"Processed {output_file_path}: {df['tokens'].iloc[0]} (type: {type(df['tokens'].iloc[0][0])})")

input_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenized_data"
output_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenized_data_eos/"

process_csv_files(input_folder, output_folder)

