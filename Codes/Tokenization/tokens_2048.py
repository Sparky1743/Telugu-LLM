import os
import pandas as pd

def split_tokens(tokens, chunk_size=2048):
    """Yield chunks of tokens list of size chunk_size."""
    for i in range(0, len(tokens), chunk_size):
        yield tokens[i:i + chunk_size]

def process_csv_files(parent_folder, output_folder, chunk_size=2048, row_limit=1000):
    os.makedirs(output_folder, exist_ok=True)
    
    output_data = []
    current_tokens = []
    output_row_index = 0  # Track the output row index for split indication
    file_count = 1  # File counter for naming output files
    csv_count = 0  # Counter for the number of CSV files processed

    total_csv_files = sum(len([file for file in files if file.endswith('.csv')]) for _, _, files in os.walk(parent_folder))
    print(f"Total CSV files to process: {total_csv_files}")

    for root, _, files in os.walk(parent_folder):
        for file in sorted(files):  # Sort files to ensure consistent processing order
            if file.endswith('.csv'):
                input_file = os.path.join(root, file)
                print(f"\nProcessing {input_file}...")
                
                # Increment CSV count
                csv_count += 1
                
                df = pd.read_csv(input_file)
                
                for i, tokens_str in enumerate(df['tokens']):
                    # Convert string of tokens back to a list
                    tokens = eval(tokens_str) if isinstance(tokens_str, str) else tokens_str
                    
                    current_tokens.extend(tokens)
                    
                    while len(current_tokens) >= chunk_size:
                        chunk = current_tokens[:chunk_size]
                        output_data.append(chunk)  # Append the 2048-token chunk
                        output_row_index += 1
                        current_tokens = current_tokens[chunk_size:]  # Remove used tokens from buffer
                        
                        if len(output_data) >= row_limit:
                            output_file = os.path.join(output_folder, f'processed_tokens_{file_count}.csv')
                            pd.DataFrame({'tokens_2048': output_data}).to_csv(output_file, index=False)
                            print(f"Saved {output_file} with {len(output_data)} rows.")
                            
                            output_data = []
                            file_count += 1
                
                print(f"End of {file} reached.")
                if current_tokens:
                    print(f"Tokens remaining from last row of {file}: {len(current_tokens)}")
                    print(f"Carrying over {len(current_tokens)} tokens to the next CSV.")
                    print(f"Next input CSV starts at processed CSV row {output_row_index}.")

    # After all files are processed, handle any remaining tokens
    if current_tokens:
        output_data.append(current_tokens)
        print(f"Final tokens carried over in last row: {len(current_tokens)}")

    # Save any remaining rows in output_data to a final CSV file
    if output_data:
        output_file = os.path.join(output_folder, f'processed_tokens_{file_count}.csv')
        pd.DataFrame({'tokens_2048': output_data}).to_csv(output_file, index=False)
        print(f"Saved {output_file} with {len(output_data)} rows.")
    
    # Final confirmation message
    if csv_count == total_csv_files:
        print(f"\nAll {total_csv_files} CSV files have been successfully processed.")
    else:
        print(f"\nWarning: Only {csv_count} out of {total_csv_files} CSV files were processed.")

parent_folder = '/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokenized_data_eos'   
output_folder = '/nlsasfs/home/aipsc/myksingh/telugu_llm/Telugu_Tokens_2048'   
process_csv_files(parent_folder, output_folder, row_limit=50000)
