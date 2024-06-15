import json

def read_jsonl(file_path, num_lines=10):
    with open(file_path, 'r') as file:
        for i in range(num_lines):
            line = file.readline()
            if not line:
                break
            try:
                json_data = json.loads(line.strip())
                print(json.dumps(json_data, indent=2))  # Pretty print the JSON
            except json.JSONDecodeError:
                print(f"Error decoding JSON on line {i + 1}")

# Change the path to your JSONL file and the number of lines you want to read
file_path = 'te_1.jsonl'
read_jsonl(file_path, num_lines=10)
