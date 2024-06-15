import os
import pandas as pd

folder_path = '/home/llmtelugu/code/vartha/csv'

dataframes = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

unique_df = combined_df.drop_duplicates()

output_file = '1.csv'
unique_df.to_csv(output_file, index=False)

print(f'Unique entries have been written to {output_file}')
