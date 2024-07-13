import os

# Function to delete files from a list of paths
def delete_files(file_paths, original_dir, target_dir):
    for original_file_path in file_paths:
        try:
            # Get relative path from the original directory
            relative_path = os.path.relpath(original_file_path, original_dir)
            # Form the target file path based on the relative path
            target_file_path = os.path.join(target_dir, relative_path)
            # Remove the file from the target directory
            os.remove(target_file_path)
            print(f"Deleted: {target_file_path}")
        except FileNotFoundError:
            print(f"File not found: {target_file_path}")
        except Exception as e:
            print(f"Error deleting {target_file_path}: {e}")

# Read file paths from a text file
def read_file_paths(file_name):
    with open(file_name, 'r') as file:
        file_paths = file.readlines()
    return [path.strip() for path in file_paths]

# Main function to execute the deletion
if __name__ == "__main__":
    # file_name = 'file_paths.txt'  # Replace with the name of your file
    # original_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/view"
    # target_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/view2"
    file_name = "/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/Logs/removed_files.txt"
    original_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_new"
    target_dir = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunks_dedup"

    
    # Read the file paths from the text file
    file_paths = read_file_paths(file_name)
    
    # Delete the files from the target directory
    delete_files(file_paths, original_dir, target_dir)
