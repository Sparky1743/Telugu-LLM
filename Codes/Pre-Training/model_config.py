from transformers import AutoModelForCausalLM, GemmaConfig, AutoTokenizer, AutoModel, MistralConfig, MistralModel, MistralForCausalLM, LlamaConfig, LlamaForCausalLM
import torch
import torch.nn as nn
import torch.nn.init as init
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("/raid/telugu_llm/Tokenizer")

print(len(tokenizer.vocab))

config = MistralConfig(hidden_size=2048,
                     vocab_size=len(tokenizer.vocab),
                     num_attention_heads=32,
                     num_key_value_heads=8,
                     num_hidden_layers=16,
                     intermediate_size=7168,
                     eos_token_id=3,
                     bos_token_id=6,
                     pad_token_id =0,
                     sliding_window=2048,
                     max_position_embeddings=2048,)

model_mis = MistralForCausalLM(config=config).to(dtype=torch.bfloat16)

print(next(model_mis.parameters()).dtype)

for i,j in model_mis.named_parameters():
    if j.requires_grad and len(j.size()) > 1:
        init.xavier_uniform_(j.data)

total_param=0
for i,j in model_mis.named_parameters():
    total_param += j.numel()
print(total_param/(10**9))

model_mis.save_pretrained("/raid/telugu_llm") # change path if needed
print("Model Saved")
