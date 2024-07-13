import csv

def read_csv(file_path, num_lines=10):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        line_count = 0
        for row in reader:
            if line_count >= num_lines:
                break
            print(row)
            line_count += 1
            

# Change the path to your CSV file and the number of lines you want to read
file_path = r'D:\SSD-files\Telugu LLM\Codes\parquet_converter\csv\train-00000-of-00005-aba1181cb685e9bb.csv'
read_csv(file_path, num_lines=10)
