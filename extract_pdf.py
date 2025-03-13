from pypdf import PdfReader
import os

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += page.extract_text() + "\n"
        print(f"Extracted page {i+1}/{len(reader.pages)} from {os.path.basename(pdf_path)}")
    return text

if __name__ == "__main__":
    # Replace with your PDF paths
    pdf_paths = ["hr.pdf", "hr2.pdf"]

    
    all_text = ""
    for pdf_path in pdf_paths:
        print(f"Processing {pdf_path}...")
        pdf_text = extract_text_from_pdf(pdf_path)
        all_text += pdf_text + "\n\n"
    
    # Save the extracted text to a file
    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(all_text)
    
    print(f"Extraction complete! Saved to extracted_text.txt")
    print(f"Total characters extracted: {len(all_text)}")