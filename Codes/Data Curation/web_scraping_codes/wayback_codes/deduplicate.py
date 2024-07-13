import os
import pandas as pd
from datetime import datetime

def remove_overlapping_links(df):
    df['short_link'] = df['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1])
    df = df.drop_duplicates(subset='short_link', keep='first')
    df = df.drop(columns=['short_link'])
    return df

def clean_csv_directory(csv_directory):
    all_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    
    if len(all_files) == 1:
        print("Only one file, no need to remove duplicates")
        return
    
    # Sort files by date, assuming the filename starts with YYYYMMDD
    all_files.sort()
    
    # Read all CSV files into DataFrames
    df_list = []
    for file in all_files:
        file_path = os.path.join(csv_directory, file)
        df = pd.read_csv(file_path)
        df['source_file'] = file  # Add a column to keep track of the source file
        df_list.append(df)
    
    # Combine all DataFrames except the latest one
    combined_df = pd.concat(df_list[:-1], ignore_index=True)
    combined_df = remove_overlapping_links(combined_df)
    
    # Get the latest file DataFrame
    latest_file = all_files[-1]
    latest_file_path = os.path.join(csv_directory, latest_file)
    latest_df = pd.read_csv(latest_file_path)
    latest_df['short_link'] = latest_df['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1])
    
    # Remove overlapping links from the latest DataFrame
    previous_links = set(combined_df['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1]))
    latest_df = latest_df[~latest_df['short_link'].isin(previous_links)]
    latest_df = latest_df.drop(columns=['short_link'])
    
    # Save the cleaned latest DataFrame back to its CSV file
    latest_df.to_csv(latest_file_path, index=False)
    print(f"Cleaned data written to {latest_file}")
    
    # Remove 'source_file' column and save back the previous DataFrames
    for df in df_list[:-1]:
        file = df['source_file'].iloc[0]
        file_path = os.path.join(csv_directory, file)
        df = df.drop(columns=['source_file'])
        df.to_csv(file_path, index=False)
        print(f"Cleaned data written to {file}")

# Example usage
corpus_dir = '/home/llmtelugu/test/created_csvs'
clean_csv_directory(corpus_dir)
