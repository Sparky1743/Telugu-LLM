import csv
import re
import os
import pickle

csv.field_size_limit(10000000000)

def extract_english_segments(text):
    # Regular expression to find segments of English text, numbers, and symbols including spaces
    segments = re.findall(r'[a-zA-Z0-9»!@#$%^&*()_+={}\[\]:;"\'|\\<,>.?/~\s\n%+^-]+', text)
    
    remove_list = []
    remove_this = ""
    detect = False
    
    for i in segments:
        if i != " ":
            remove_this += i
            detect = True
        else:
            if detect:
                remove_list.append(remove_this)
                remove_this = ""
            detect = False
            
    # Adding the last segment if it exists
    if remove_this:
        remove_list.append(remove_this)

    return remove_list

def process_csv(input_file, output_log):
    results = {}

    with open(input_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        with open(output_log, mode='w', encoding='utf-8') as log_file:
            for row in csv_reader:
                content = row['content']
                english_segments = extract_english_segments(content)
                
                # Write to log file
                if english_segments:
                    log_file.write(f"ID: {row['id']}\n")
                    segment_list = []

                    for segment in english_segments:
                        if len(segment.replace(" ", "")) > 6:
                            is_alp = re.findall(r'[a-zA-Z]+', segment)
                            if len(is_alp) > 0:
                                log_file.write(f"English Text: {segment}\n")
                                segment_list.append(segment)

                    log_file.write("\n")
                    if segment_list:
                        results[row['id']] = segment_list

    return results

if __name__ == "__main__":
    name = "gultetelugu"
    input_file = f'/nlsasfs/home/aipsc/myksingh/llmtelugu/codes/data_processing_codes/test/deleted_folder/{name}.csv'  # Replace with your CSV file path
    output_log = f'/nlsasfs/home/aipsc/myksingh/llmtelugu/codes/data_processing_codes/test/deleted_folder{name}.txt'  # Replace with desired log file path
    results = process_csv(input_file, output_log)
    
    # keys = list(results.keys())
    # print(f"First entry: {keys[0]}: {results[keys[0]]}")
    # print(f"Second entry: {keys[1]}: {results[keys[1]]}")
    # print(f"Second entry: {keys[2]}: {results[keys[2]]}")

    # Save the results dictionary to a pickle file
    pickle_folder = "/nlsasfs/home/aipsc/myksingh/llmtelugu/codes/data_processing_codes/test/deleted_folder"
    pickle_file = os.path.join(pickle_folder, f'{name}.pkl')

    with open(pickle_file, 'wb') as f:
        pickle.dump(results, f)
    
    print(f"Results dictionary saved to {pickle_file}")