import pandas as pd

def count_overlapping_links(file1, file2):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Create a short_link column in both DataFrames
    df1['short_link'] = df1['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1])
    df2['short_link'] = df2['link'].apply(lambda x: x.split('https://www.eenadu.net')[-1])
    
    # Find overlapping short links
    overlapping_links = pd.merge(df1[['short_link']], df2[['short_link']], on='short_link', how='inner')
    print(overlapping_links)
    
    # Return the number of overlapping links
    return len(overlapping_links)

# Example usage
file1 = '/home/llmtelugu/data/wayback_data/eenadu/eenaducsv/created_csvs/20240104.csv'
file2 = '/home/llmtelugu/data/wayback_data/eenadu/eenaducsv/created_csvs/20240112.csv'
num_overlapping_links = count_overlapping_links(file1, file2)
print(f'Number of overlapping links: {num_overlapping_links}')

