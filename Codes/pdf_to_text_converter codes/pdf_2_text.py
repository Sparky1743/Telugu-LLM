import pytesseract
from pdf2image import convert_from_path
import re
import os

def extract_telugu_text_from_pdf(pdf_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    telugu_text = ""
    # Pattern to include Telugu characters, digits, whitespace, punctuation, and special characters
    telugu_pattern = re.compile(r'[\u0C00-\u0C7F\d\s.,#?%*/\\(){}\[\]\-+&]+', re.UNICODE)

    for i, image in enumerate(images):
        # Perform OCR on the image
        text = pytesseract.image_to_string(image, lang='tel')
        print(f"Page {i + 1} text: {text[:100]}...")  # Print first 100 characters for debugging

        # Find all Telugu text and other specified characters in the page
        matches = telugu_pattern.findall(text)
        if matches:
            telugu_text += " ".join(matches) + "\n"
            print(f"Page {i + 1} matches: {matches}")

    return telugu_text

def process_pdfs_in_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate over all files in the specified folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Processing {pdf_path}")
            extracted_telugu_text = extract_telugu_text_from_pdf(pdf_path)

            # Create a text file with the same name as the PDF in the output folder
            text_filename = os.path.splitext(filename)[0] + ".txt"
            text_filepath = os.path.join(output_folder, text_filename)
            with open(text_filepath, "w", encoding="utf-8") as file:
                file.write(extracted_telugu_text)

            print(f"Saved extracted text to {text_filepath}")

# Example usage
input_folder = "/Users/pavandeekshith/B-Tech/TeluguLLM/data/data_pdfs"
output_folder = "/Users/pavandeekshith/B-Tech/TeluguLLM/data/data_txt"
process_pdfs_in_folder(input_folder, output_folder)

print("Telugu text extraction complete for all PDFs in the folder.")


# You should download tesseract -lang idi leka pothe error vastundi