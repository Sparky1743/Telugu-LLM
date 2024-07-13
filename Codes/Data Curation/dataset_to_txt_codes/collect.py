import os

def merge_txt_files(input_folder, output_file):
    if not os.path.isdir(input_folder):
        raise FileNotFoundError(f"The specified input folder does not exist: {input_folder}")

    # Collect all .txt files in the folder
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in the specified folder: {input_folder}")

    # Merge the contents of all .txt files
    merged_content = ""
    for txt_file in txt_files:
        txt_file_path = os.path.join(input_folder, txt_file)
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            merged_content += file.read() + "\n"

    # Save the merged content to the specified output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(merged_content)

    print(f"All .txt files have been successfully merged into {output_file}")

input_folder = r'C:\Users\birud\Downloads\train\train'  # Replace with the path to your folder
output_file = r'C:\Users\birud\Downloads\text\train.txt'  # Replace with the desired output file path

merge_txt_files(input_folder, output_file)
