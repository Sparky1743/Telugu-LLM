import os
import zipfile

def zip_folder(folder_path, output_path):
    output_dir = os.path.dirname(output_path)
    
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

folder_path = '/home/llmtelugu/data'
output_path = '/home/llmtelugu/dataoutput.zip'
zip_folder(folder_path, output_path)
