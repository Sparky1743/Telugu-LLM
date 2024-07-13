import pandas as pd

input_csv_path = '/home/llmtelugu/data/webdunia/Debug/failed_links_2.csv'

output_csv_path = '/home/llmtelugu/data/webdunia/Debug/failed_links_3.csv'

df = pd.read_csv(input_csv_path)

df.drop(df.columns[0], axis=1, inplace=True)

df.to_csv(output_csv_path, index=False)

print(f"CSV file with the second column removed saved to {output_csv_path}")
