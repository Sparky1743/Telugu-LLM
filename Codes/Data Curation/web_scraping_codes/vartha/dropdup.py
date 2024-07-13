import pandas as pd

input_csv_path = '/home/llmtelugu/code/vartha/1.csv'

output_csv_path = '/home/llmtelugu/code/vartha/1.csv'

df = pd.read_csv(input_csv_path)

df.drop(df.columns[1], axis=1, inplace=True)

df.to_csv(output_csv_path, index=False)

print(f"CSV file with the second column removed saved to {output_csv_path}")
