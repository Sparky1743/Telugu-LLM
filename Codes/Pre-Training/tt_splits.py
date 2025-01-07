from datasets import load_dataset, concatenate_datasets

df_1 = load_dataset("parquet", data_files="/raid/telugu_llm/rewriting_reality/telugu/Tokens_2048_without_unk_combined_parquet/combined_dataset.parquet")["train"]

df_2 = load_dataset("parquet", data_files="/raid/telugu_llm/rewriting_reality/english/Tokens_2048_without_unk_combined_parquet/combined_dataset.parquet")["train"]

df_1_split = df_1.train_test_split(test_size=5000)
df_2_split = df_2.train_test_split(test_size=1000)

df = concatenate_datasets([df_1_split["train"], df_2_split["train"]])

print(df_1)
print(df_2)

print(df)

df = df.shuffle(seed=42)

df.to_parquet("/raid/final_dataset/Train_Final.parquet")
df_2_split["test"].to_parquet("/raid/final_dataset/English_test.parquet")
df_1_split["test"].to_parquet("/raid/final_dataset/Telugu_test.parquet")
