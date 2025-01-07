from transformers import AutoModelForCausalLM, AutoTokenizer
    
tokenizer = AutoTokenizer.from_pretrained("/raid/telugu_llm/Tokenizer")
model = AutoModelForCausalLM.from_pretrained("/raid/telugu_pretrain_results/checkpoint-207000", device_map="cpu")

input_text = "Hello world"
input_ids = tokenizer.encode(input_text,
            return_tensors="pt")

outputs = model.generate(input_ids, max_new_tokens=100, do_sample=True)

print(tokenizer.decode(outputs[0]))
