import os

def get_text_files_info(folder_path):
    total_size = 0
    file_sizes = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
            total_size += file_size
            file_sizes[file_name] = file_size
    return total_size, file_sizes

folder_path = "/home/llmtelugu/data/sakshi_data/text_data"
total_text_size_mb, file_sizes_mb = get_text_files_info(folder_path)

print("Size of each individual text file:")
for file_name, file_size_mb in file_sizes_mb.items():
    print(f"{file_name}: {file_size_mb:.2f} MB")

print(f"number of txt files = {len(file_sizes_mb.items())}")
print(f"Total size occupied by text files in {folder_path}: {total_text_size_mb:.2f} MB")
