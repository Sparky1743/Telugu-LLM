import pandas as pd
import re
import os
import tqdm

# Function to clean text by removing unnecessary characters
def clean_text(text):
    # Remove digits (0-9) and commas directly after digits
    text = re.sub(r'\d,?', '', text)
    
    # Remove special token <|hyperlink|>
    text = re.sub(r'<\|hyperlink\|>', '', text)
    
    # Remove emojis using regex (covering a broad range of Unicode emoji characters)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002600-\U000026FF"  # miscellaneous symbols
        u"\U00002700-\U000027BF"  # additional miscellaneous symbols
        u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        u"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A (includes 🤣, 🥰, etc.)
        u"\U0001F1F2-\U0001F1F4"  # flags
        u"\U0001F1E6-\U0001F1FF"  # flags continued
        u"\U00002500-\U00002BEF"  # various symbols
        u"\U0001F004"             # Mahjong tile red dragon
        u"\U0001F0CF"             # playing card black joker
        "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'', text)
    

    # Some more wild card patterns
    latin_chars_pattern = re.compile(r'[ñफóŒŠçìíæÐČąěňōŗřůžǎǐ£ð«»ứṟṇṅṃḻḍৰ]', flags=re.UNICODE)

    text = latin_chars_pattern.sub(r'', text)

    pattern = re.compile(r'[0-9¡¢¤¥§©¬­®°±¶·¿ÀÁडÂफÃÄÅÆÇÈÉÊËÌÍÎÑÔÕÖ×ØÙÚÛÜÞßàáâäèéêëîïòôõö÷ùúüýþĀāćĒēęĞğĪīĮįİıļĽľłńŚśŞşšŪūŸŽəɛɡʹʾʿˆː̧́̃̄̆̇̈̊ΔΩήίαβγδεηλμνοπρςστυφόБабвгдежзийклмнопрстуфхцчшщыьэюяאבהויצת،ؚ؟ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهوىيًُِّٹپچڈڑژښکګگںھہۃیےۓ۔ँंःअआइईउऊएओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलळवशषसह़ऽािीुूृॅेैॉोौ्।॥॰এগডনু੍ਂਡਦਰਵਹਾੇછતનમસાિેૐஅஆஇஉஎஏஒகஙசஜடணதநனபமயரறலளழவஶஷஸாிீுூெேைொோ]', flags=re.UNICODE)

    text = pattern.sub(r'', text)

    pattern2 = re.compile(r'[\u0D00-\u0D7F\u0D80-\u0DFF\u0E00-\u0E7F\u0E80-\u0EFF\u1000-\u109F\u1A00-\u1A1F\u1B00-\u1B7F\u2C00-\u2C5F\u3000-\u303F\u4E00-\u9FFF\uAC00-\uD7AF\uF900-\uFAFF\uFE10-\uFE1F\uFE30-\uFE4F\uFF00-\uFFEF\uD800-\uDBFF][^\u0D00-\u0D7F\u0D80-\u0DFF\u0E00-\u0E7F\u0E80-\u0EFF\u1000-\u109F\u1A00-\u1A1F\u1B00-\u1B7F\u2C00-\u2C5F\u3000-\u303F\u4E00-\u9FFF\uAC00-\uD7AF\uF900-\uFAFF\uFE10-\uFE1F\uFE30-\uFE4F\uFF00-\uFFEF\uD800-\uDBFF]*', flags=re.UNICODE)
    
    text = pattern2.sub(r'', text)

    pattern3 = re.compile(r'[គងឌថទធមសḷṣṭἀἜ⊗⊛⌨⍟⏳￼𓃵🟆�čĐĺœɑɾάέύιऐडफ఩スプラワン﻿]', flags=re.UNICODE)
    text = pattern3.sub(r'', text)

    pattern4 = re.compile(r'[ಅ-ಹಾ-್]+', flags=re.UNICODE)
    text = pattern4.sub(r'', text)

    pattern5 = re.compile(r'[À-ÿɐɻʋΒζμঘদমরসাী্ਰ৳ਟਥਬੀੋ்ᱩᱱṛडफ]', flags=re.UNICODE)
    text = pattern5.sub(r'', text)

    pattern6 = re.compile(r'[ٽڕڪڵۆێە]', flags=re.UNICODE)
    text = pattern6.sub(r'', text)

    return text

def clean_csv(file_path):
    df = pd.read_csv(file_path)
    
    if 'content' in df.columns:
        df['content'] = df['content'].apply(lambda x: clean_text(str(x)) if isinstance(x, str) else x)
    
    df.to_csv(file_path, index=False)
    print(f"Processed and overwritten: {file_path}")

def process_folder(folder_path):
    for filename in tqdm.tqdm(os.listdir(folder_path), desc="Processing Files"):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            clean_csv(file_path)

folder_path = '/nlsasfs/home/aipsc/myksingh/telugu_llm/Train_Tokenizer/Final_2'  
process_folder(folder_path)
