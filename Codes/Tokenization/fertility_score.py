from transformers import AutoTokenizer
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import argparse
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--tokenizer_path", type=str, required=True, help="Path to the tokenizer.")
parser.add_argument("--data_path", type=str, required=True, help="Path to the folder containing CSV files.")
parser.add_argument("--column_name", type=str, required=True, help="Column name to extract content from.")
args = parser.parse_args()

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path)

csv_files = [f for f in os.listdir(args.data_path) if f.endswith(".csv")]

if not csv_files:
    raise ValueError("No CSV files found in the specified folder.")

fertility_scores = []

for filename in tqdm(csv_files, desc="Processing CSV files"):
    file_path = os.path.join(args.data_path, filename)
    
    try:
        df = pd.read_csv(file_path)
        
        if args.column_name not in df.columns:
            print(f"Warning: Column '{args.column_name}' not found in {filename}. Skipping file.")
            continue
        
        content_list = df[args.column_name].fillna('').astype(str).tolist()

        df_word_count = [len(word_tokenize(content)) for content in content_list]
        np_word_count = np.array(df_word_count)

        token_list = tokenizer(content_list)["input_ids"]

        token_count = [len(tokens) for tokens in token_list]
        np_token_count = np.array(token_count)

        f_score = np.mean(np.divide(np_token_count, np_word_count, where=np_word_count!=0))

        fertility_scores.append(f"{filename}: {f_score}")
    
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        continue  # Skip to the next file in case of an error

output_path = "/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenizer/Fertility_scores.txt"
with open(output_path, "w") as file:
    for score in fertility_scores:
        file.write(score + "\n")

print(f"Fertility scores calculated and saved for {len(fertility_scores)} files.")
