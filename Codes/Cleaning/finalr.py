import csv
import pickle
import os

csv.field_size_limit(10000000000)

def remove_strings_from_row(row, content, strings_to_remove):
    # for string in strings_to_remove:
    #     print(string)
    # print("row", row,":", strings_to_remove)
    # if len(strings_to_remove) > 0 and (strings_to_remove[-1] == " " or strings_to_remove[-1] == "\n" or strings_to_remove[-1] == "»"):
    #     content = content.replace(strings_to_remove[:-1], '')
    # else:
    #     content = content.replace(strings_to_remove, '')

    if len(strings_to_remove) > 0 and (("https" in strings_to_remove) or ("www" in strings_to_remove) or ("http" in strings_to_remove) or ("http://" in strings_to_remove)):
        if strings_to_remove[-1] == " " or strings_to_remove[-1] == "\n" or strings_to_remove[-1] == "»":
            content = content.replace(strings_to_remove[:-1], ' <|hyperlink|> ')
        else:
            content = content.replace(strings_to_remove, ' <|hyperlink|> ')
    return content

def modify_csv(input_file, pickle_file, output_file):
    # Load the dictionary from the pickle file
    with open(pickle_file, 'rb') as f:
        removal_dict = pickle.load(f)
    
    # Open the input CSV file and the output CSV file
    with open(input_file, mode='r', encoding='utf-8') as csv_file, open(output_file, mode='w', encoding='utf-8') as out_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        for row in csv_reader:
            row_id = row['id']
            if row_id in removal_dict:
                content = row['content']
                for i in removal_dict[row_id]:
                    for j in range(15):
                        # print(row_id, i[:len(i) - j])
                        rem_content = remove_strings_from_row(row_id, content, i[:len(i) - j])
                        rem_content2 = remove_strings_from_row(row_id, content, i[j:len(i)])
                        # rem_content3 = remove_strings_from_row(row_id, content, i[j:len(i) - j])
                        if len(content) != len(rem_content):
                            content = rem_content
                            break
                        elif len(content) != len(rem_content2):
                            content = rem_content2
                            break
                        # elif len(content) != len(rem_content3):
                        #     content = rem_content3
                        #     break
                        else:
                            continue
                row['content'] = content
            csv_writer.writerow(row)

if __name__ == "__main__":
    name = "gultetelugu"
    input_file = f'/nlsasfs/home/aipsc/myksingh/llmtelugu/codes/data_processing_codes/test/deleted_folder/{name}.csv'  # Replace with your input CSV file path
    pickle_file = f'/nlsasfs/home/aipsc/myksingh/llmtelugu/codes/data_processing_codes/test/deleted_folder/{name}.pkl'  # Replace with your pickle file path
    output_file = f'/nlsasfs/home/aipsc/myksingh/llmtelugu/final_processing/cleaning/websites/websites_cleaned/cleaned_{name}_batch2.csv'  # Replace with your output CSV file path

    modify_csv(input_file, pickle_file, output_file)
    
    print(f"Modified CSV saved to {output_file}")
