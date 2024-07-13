import pandas as pd
import os
import subprocess
import tqdm

# -1 to all values in return_rows
def return_rows(input_csv):
    # df = pd.read_csv(input_csv)
    lst2 = []
    # print(input_csv)
    # print("###################")
    lst = subprocess.run(f"cat {input_csv}  | cut -d ',' -f1", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split("\n")[:-1]
    # print(input_csv)
    for i in lst:
        lst2.append(int(i) - 1)
    return lst2


folder_path_ori = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV"
folder_path_rem = "/nlsasfs/home/aipsc/myksingh/llmtelugu/final_pre_pro/CSV"
folder_path_ret = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV_remaining"
folder_path_out2 = "/nlsasfs/home/aipsc/myksingh/llmtelugu/chunk_json/chunks_dedup/CSV_removed"

for filename in tqdm.tqdm(os.listdir(folder_path_ori), desc = "processing"):
    if filename.endswith(".csv"):
        input_csv_rem_csv = os.path.join(folder_path_rem, filename)
        input_csv_ori_csv = pd.read_csv(os.path.join(folder_path_ori, filename))
        folder_path_ret_csv = os.path.join(folder_path_ret, filename)
        folder_path_out2_csv = os.path.join(folder_path_out2, filename)
        
        rows_to_remove = return_rows(input_csv_rem_csv)
        df_r_o_r = input_csv_ori_csv.iloc[rows_to_remove, :]
        print(len(df_r_o_r))
        input_csv_ori_csv.drop(rows_to_remove, inplace = True)
        df_r_o_r.to_csv(folder_path_ret_csv, index = False)
        input_csv_ori_csv.to_csv(folder_path_out2_csv, index = False)
        
        # remove_rows_from_csv(input_csv_ori, rows_to_remove, output_csv_ret)
