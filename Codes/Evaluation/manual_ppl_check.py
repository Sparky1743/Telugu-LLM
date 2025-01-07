import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Paths
csv_path = "/nlsasfs/home/aipsc/myksingh/telugu_llm/latest_news/top_10_scores/m_news_70/top_10.csv"  # Replace with the path to your CSV file
output_folder = "/nlsasfs/home/aipsc/myksingh/telugu_llm/latest_news/actual_outs/news_70/airavata"  # Replace with the path to your output folder

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the model and tokenizer
model_name = "/nlsasfs/home/aipsc/myksingh/telugu_llm/airavata 7b"
tokenizer_path = "/nlsasfs/home/aipsc/myksingh/telugu_llm/airavata 7b"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
model = AutoModelForCausalLM.from_pretrained(model_name)

model.eval()

# Read the CSV file
df = pd.read_csv(csv_path)

# Process each row in the content column
for idx, row in df.iterrows():
    input_text = row['content']  # Ensure the column name matches your CSV
    
    inputs = tokenizer(input_text, return_tensors="pt")
    input_ids = inputs["input_ids"]

    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
    
    # Calculate perplexity
    perplexity = torch.exp(outputs.loss).item()

    # Decode learned sentence
    learned_sentence = tokenizer.decode(outputs.logits.argmax(dim=-1)[0])

    # Prepare output
    output_content = (
        f"Original Sentence:\n{input_text}\n\n"
        f"Perplexity: {perplexity}\n\n"
        f"Learned Sentence:\n{learned_sentence}\n"
    )

    # Save to a .txt file
    output_file_path = os.path.join(output_folder, f"output_{idx}.txt")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(output_content)

    print(f"Processed row {idx} and saved output to {output_file_path}")
