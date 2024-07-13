import pandas as pd
name = "gultetelugu"
df = pd.read_csv(f"/nlsasfs/home/aipsc/myksingh/llmtelugu/final_processing/cleaning/websites/websites_cleaned/cleaned_{name}_batch2.csv")

df = df[~df.iloc[:, 1].str.contains("https", na=False)]
df = df[~df.iloc[:, 1].str.contains("www", na=False)]
df = df[~df.iloc[:, 1].str.contains("http", na=False)]


df.to_csv(f"/nlsasfs/home/aipsc/myksingh/llmtelugu/final_processing/more_cleaning/websites/more_cleaned_{name}.csv", index=False)

print("completed")
