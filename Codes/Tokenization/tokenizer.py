import os
from tqdm import tqdm
import time
import argparse
from tokenizers import SentencePieceBPETokenizer
from transformers import PreTrainedTokenizerFast
import datetime
import pandas as pd
from tokenizers.normalizers import Replace 
from tokenizers import decoders 

# Get current date
date = datetime.datetime.now().strftime("%Y-%m-%d")
print(date)

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--vocab", type=int, default=32768)  # Changed to int
parser.add_argument("--data", type=str, default=".")
parser.add_argument("--save_path", type=str, default="./tokenizer_v1")
args = parser.parse_args()

# Change bos & eos
bos_tok = "<bos>"
eos_tok = "<eos>"
# Add basic characters to this list, including numbers & special language characters.
numbers_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

hash_list = ["#", "##", "###"]

telugu_numbers = ["౦", "౧", "౨", "౩", "౪", "౫", "౬", "౭", "౮", "౯"]

extra_char = numbers_list + hash_list + telugu_numbers

# Ensure you remove characters not related to your language
if os.path.isdir(args.data):
    file_paths = []
    for root, dirs, files in os.walk(args.data):
        for file in files:
            file_paths.append(os.path.join(root, file))
else:
    file_paths = [args.data]

print(file_paths)

def train_tokenizer(text_list, vocab_size=32768, model_name="./telugu_tokenizer_v1"):
    st = time.time()
    print(f'Vocab size: {vocab_size}')
    print("Length of directory path", len(file_paths))
    print(f"Model name : {model_name}")

    tokenizer = SentencePieceBPETokenizer()
    
    for file_name in text_list:
        df = pd.read_csv(file_name).iloc[:, 0].dropna()
        df = df.str.replace(r'\d+', '', regex=True)  # Remove numbers
        text_data = df.tolist()  # Convert to a list of strings

        print(f"Training on {len(text_data)} entries from {file_name}")  # Debugging output
        
        try:
            tokenizer.train_from_iterator(
                iter(text_data),  # Ensure it's an iterator
                vocab_size=int(vocab_size),
                min_frequency=5,
                special_tokens=["<pad>", "<cls>", "<sep>", eos_tok, "<mask>", "<unk>", bos_tok, "<user>", "<assistant>"] + extra_char,
                show_progress=True,
            )
        except Exception as e:
            print("Error in training tokenizer", e)
            print("Trained for {} minutes".format((time.time()-st)/60)) 
            continue  # Continue to the next file
        
        print("File " + file_name + " Completed")

    et = time.time()
    print("Trained {} in {} minutes".format(model_name, (et - st) / 60))

    tokenizer.save_model(".", "my_tokenizer")

    # Don't forget to add special tokens.
    transformer_tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        bos_token=bos_tok,
        eos_token=eos_tok,
        unk_token="<unk>",
        pad_token="<pad>",
        mask_token="<mask>",
        padding_side="left",
        truncation_side="right",
        additional_special_tokens=["<user>", "<assistant>"],
        clean_up_tokenization_spaces=False,
    )

    transformer_tokenizer.backend_tokenizer.normalizer = Replace(' ', '▁')
    transformer_tokenizer.backend_tokenizer.pre_tokenizer = None
    transformer_tokenizer.backend_tokenizer.decoder = decoders.Replace('▁', ' ')
    
    transformer_tokenizer.save_pretrained(model_name)
    print("Saved {} in {} minutes".format(model_name, (time.time()-et)/60))

# Train the tokenizer with the provided file paths and vocab size
train_tokenizer(file_paths, args.vocab, model_name=args.save_path)
