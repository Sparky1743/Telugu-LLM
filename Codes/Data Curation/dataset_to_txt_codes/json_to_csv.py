import json
import csv

def jsonl_to_csv(jsonl_file_path, csv_file_path):
    with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
        # Read the first line to get the headers
        first_line = jsonl_file.readline()
        first_obj = json.loads(first_line)
        headers = first_obj.keys()
        
        # Move the cursor back to the beginning of the file
        jsonl_file.seek(0)
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
            csv_writer.writeheader()
            
            for line in jsonl_file:
                json_obj = json.loads(line)
                csv_writer.writerow(json_obj)
i = "te_clean_0000"
jsonl_to_csv(rf'D:\SSD-files\Telugu LLM\Codes\parquet_converter\parquets\{i}.jsonl', rf'D:\SSD-files\Telugu LLM\Codes\parquet_converter\csv\{i}.csv')
