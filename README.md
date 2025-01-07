<p>Note: All the codes are in Codes folder.</p>
<h3>Data Curation:</h3>
<p>Codes for scraping data from various sites, converting pdfs to text and extracting text from existing datasets. List has been mentioned in the excel sheet.</p>

<h3>Data Deduplication:</h3>
<p>Note: it is necessary to have your dataset as only chunks of text files for the deduplication codes to work. Also it is better to have large number of these text files for efficient deduplication, hence it is recommended to curate your data article wise (each article in a txt file). </p>

<ol>
  <li><strong>hash.py</strong></li>
  <p>It finds all the text files in the given folder and generates their hash values using sim hash algorithm. These hash values are written in CSV files.</p>
 
  <li><strong>similarity_check.py</strong></li>
  <p>It basically does intra folder comparision of the hash values i.e. it will drop <strong>exact</strong> duplicates (retaining one instance) from each individual CSV which were created in the previous hash.py code.</p>
  
  <li><strong>copy_after.py</strong></li>
  <p>It copies the files remaining in the previous step to a specified folder for further processing.</p>
  
  <li><strong>minhash2_6.py</strong> -> from this code onwards, we start inter folder deduplication</li>
  <p>It calculates min-hashes for the sim-hashes calculated in previous steps and loads these min-hashes into a model which will calculate nearset neighbours for each document. The file paths of the nearest neighbours (for each document) will be outputted into one or more csv files, depending on the number of near duplicates.</p>
 
  <li><strong>rem_filter2.py</strong></li>
  <p>Now the output of before code may have some false positives (files which are not near duplicates are also listed as near duplicates, this is the fault of the datasketch library we used, it is also clearly stated in their <a href="https://ekzhu.com/datasketch/lsh.html#">MinHash LSH documentation</a>), this code will remove false positives from the previous code's output.</p>
 
  <li><strong>remove_7.py</strong></li>
  <p>This code will take the csvs outputted before (which contains paths of documents and their neighbours) and create a final list (in a txt file) of file paths to be removed from the dataset created after copy_after.py code. </p>
 
  <li><strong>finalremove.py</strong></li>
  <p>It takes the list created before and removes them from the dataset created after copy_after.py code. Deduplication process is completed after this code, you can compress your dataset into a csv or json file (place each article in a row).</p>
</ol>

<h3>Cleaning:</h3>
<p>Note: The below codes assumes that all your data is spread in csvs and each row in any csv will be containing a single news article or similar text.</p>
<p>The file "build.json" has list of vulgar words for Telugu all other languages, <strong>feel free to update it if you find any words missing</strong>.</p>
<ol>
  
  <li><strong>info_iden_csv.py</strong></li>
  <p>It lists down index of rows in which vulgar words, dates, contacts and personal information are present.</p>
  
  <li><strong>pre_process.py</strong></li>
  <p>Using the list in step 1 it seperates out the dataset csv in two different folders (one with good data and other with bad data).</p>
 
  <li><strong>info_iden_csv_new_dates.py</strong></li>
  <p>As we were also removing rows with dates in them, this code will again takes the list of vulgar words, dates, contacts, personal information and removes the items with dates in the list and creates a new list with vulgar words, contacts, personal information excluding dates. You can use either remove_phone_nos.py or pre_process.py to split the dataset CSV into two different folders using the new list. (Note: Use this code if you want to keep dates in your dataset).</p>
  
  <li><strong>antieng.py</strong></li>
  <p>It removes rows with english words which might not be related to the orignal text basing on a threshold, which can be set (default = 7, meaning rows with more than 7 English words will be separated into another csv).</p>
  
  <li><strong>detect_promotions.py</strong></li>
  <p>It detects tags, promotions, ads & note it down in a log txt file.</p>
  
  <li><strong>finalr.py</strong></li>
  <p>Removes the detected promotions & replace the links with <|hyperlink|> token.</p>
  
  <li><strong>drop_links.py</strong></li>
  <p>It check all rows again for any remaining links (which may be missed by finalr.py) and then drops those rows.</p>
  
  <li><strong>ignore_case_bw</strong></li>
  <p>Sometimes, certain inappropriate words appear in mixed-case letters, combining both lowercase and uppercase letters (specifically in English). This code is used as a final cleanup step to create new CSV files by removing rows containing such words.</p>
  
</ol>

<h3>Tokenization:</h3>
<p>Note: The following codes assume that all your data, whether used to train the tokenizer or to test its fertility scores, is stored in CSV files, with each row in any CSV containing a single news article or similar text.</p>
<ol>
  <li><strong>remove_emotes.py</strong></li>
  <p>This code removes characters from CSV files that are not in Telugu or English, ensuring these characters do not appear in the tokenizer's vocabulary.</p>
  
  <li><strong>tokenizer.py</strong></li>
  <p>This code is used for training the tokenizer and expects a folder containing CSV files of data. Refer to <strong>frequently used cmds.txt</strong> for the terminal command to run the code.</p>
  
  <li><strong>fertility_score.py</strong></li>
  <p>This code is used to calculate the fertility scores of the trained tokenizer.</p>
  
  <li><strong>tokenize_data.py</strong></li>
  <p>This code applies the tokenizer, trained in previous steps, to the text data. It expects CSV files with id and content columns and outputs CSV files with id, content, and tokens columns, where the tokens column contains the tokenizer encodings of content column. </p>
  
  <li><strong>add_eos_token.py</strong></li>
  <p>This code adds the EOS token to each row in the tokens column. </p>
  
  <li><strong>remove_unk.py</strong></li>
  <p>The `remove_unk.py` script is designed to handle unknown tokens (`unk tokens`) that may be present in the `tokens` column of CSV files. Unknown tokens can reduce the quality of the model's output if they are included in pre-training. This script removes the designated unknown token (`5` in our case) from the `tokens` column of the CSV files generated by the previous preprocessing steps.

- The script processes CSV files and identifies the `tokens` column.
- It scans through the `tokens` column, removing all occurrences of the unknown token (`5`).
- The output is a cleaned version of the `tokens` column, free of the specified unknown token.

**Example**
- A row in the `tokens` column before processing: [24, 535, 466, 35, 5, 454, 5656]
- The row in the `tokens` column after processing: [24, 535, 466, 35, 454, 5656]
</p>

  <li><strong>tokens_2048.py</strong></li>
  <p>This code splits the entries in the tokens column into segments of exactly 2048 tokens each and saves them in output CSV files with a single column. In each CSV, each row contains a list of exactly 2048 tokens. </p>
  
  <li><strong>convert_to_parquet.py</strong></li>
  <p>This code converts the CSV files obtained from the previous step into Parquet files. </p>
  
  <li><strong>merge_datasets.py</strong></li>
  <p>This code combines all the Parquet files from the previous step into a single Parquet file. </p>
  
</ol>

<h3>Pre-Training:</h3>
<ol>
  <li><strong>tt_splits.py</strong></li>
  <p>This code is used for making train-test splits.</p>
  
  <li><strong>model_config.py</strong></li>
  <p>This script sets up and initializes a Mistral-based causal language model with custom configurations, including vocabulary size, hidden layers, attention heads etc.</p>
  
  <li><strong>model_pretrain.py</strong></li>
  <p>This script handles the pretraining of the large language model (LLM).</p>
  
</ol>

<h3>Evaluation:</h3>
<ol>
  <li><strong>model_run.py</strong></li>
  <p>This script is used for text generation using the trained language model. It takes input prompts, processes them through the model, and generates coherent and contextually relevant text outputs.</p>
  
  <li><strong>manual_ppl_check.py</strong></li>
  <p>This script calculates the perplexity score of the language model, providing a measure of how well the model predicts a given dataset. Lower perplexity indicates better predictive performance.</p>
  
</ol>
