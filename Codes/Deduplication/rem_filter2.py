import os
import pandas as pd
from tqdm import tqdm

def filter_and_save_csv(csv_file, output_dir):
    try:
        df = pd.read_csv(csv_file)

        filtered_df = df[df['similarity'] > 0.8]

        output_file = os.path.join(output_dir, os.path.basename(csv_file))
        
        # Save filtered DataFrame to the new path
        filtered_df.to_csv(output_file, index=False)

        return f"Filtered and saved {output_file}"
    except Exception as e:
        return f"Error processing {csv_file}: {str(e)}"

if __name__ == "__main__":
    # Define input and output directories
    input_dir = '/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/output/'
    output_dir = '/nlsasfs/home/aipsc/myksingh/llmtelugu/hashes/output2/'

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of CSV files in the directory
    csv_files = [os.path.join(input_dir, file_name) for file_name in os.listdir(input_dir) if file_name.endswith('.csv')]
    
    print(f"No of CSVs: {len(csv_files)}")

    # Process each CSV file in a simple loop
    for csv_file in tqdm(csv_files, desc="Filtering and Saving CSVs"):
        result = filter_and_save_csv(csv_file, output_dir)
