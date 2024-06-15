import os
import pandas as pd
import convert_par_to_csv

input_dir_1 = r'/mnt/HDFS1/llm/llmtelugu/new_parquets/ai4_bharat/samanantar'
output_dir_1 = r'/mnt/HDFS1/llm/llmtelugu/new_csv_data/ai4_bharat/samanantar'

convert_par_to_csv.main(input_dir_1, output_dir_1)

input_dir = r'/mnt/HDFS1/llm/llmtelugu/new_csv_data/ai4_bharat/samanantar'
output_dir = r'/mnt/HDFS1/llm/llmtelugu/new_dataset_data/ai4_bharat/samanantar'

os.makedirs(output_dir, exist_ok=True)

for file_name in os.listdir(input_dir):
    if file_name.endswith('.csv'):
        input_file_path = os.path.join(input_dir, file_name)
        df = pd.read_csv(input_file_path)
        
        # Create a new directory for each CSV file
        csv_output_dir = os.path.join(output_dir, file_name.replace('.csv', ''))
        os.makedirs(csv_output_dir, exist_ok=True)
        
        for idx, row in df.iterrows():
            if pd.notnull(row['tgt']) and str(row['tgt']).strip():
                output_file_name = f"chunk{idx + 1}.txt"
                output_file_path = os.path.join(csv_output_dir, output_file_name)
                
                with open(output_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(f"{row['tgt']}")
                    
                print(f"Converted row {idx + 1} of {input_file_path} to {output_file_path}")
    
    print(f"{file_name}.csv is done")
