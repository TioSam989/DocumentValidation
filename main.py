"""
Main module: main.py
Coordinates the PDF reading and date validation process.
"""

from pdf_reader import PDFReader
from date_validator import DateValidator


def main(file_path: str):
    """
    Main function to validate a PDF document.
    Args:
        file_path (str): Path to the PDF file.
    """
    print(f"Processing file: {file_path}")

    # Step 1: Extract text using PyPDF2
    text = PDFReader.extract_text_pypdf2(file_path)
    print(f"Extracted text: {text}")
    if not text:
        print("No text found with PyPDF2. Trying pdfminer.")
        text = PDFReader.extract_text_pdfminer(file_path)

    # Step 2: Fallback to OCR if necessary
    if not text:
        print("No text found with pdfminer. Trying OCR.")

        text = PDFReader.extract_text_with_ocr(file_path)

        print(f"Extracted text with OCR: {text}")
    # Step 3: Validate and extract dates
    if text:
        print("Extracted text (preview):")
        print(text[:500])  # Preview first 500 characters

        dates = DateValidator.find_dates(text)
        valid_dates = [date for date in dates if DateValidator.validate_date(date)]

        if valid_dates:
            print("Detected Valid Dates:")
            for date in valid_dates:
                print(date)
        else:
            print("No valid dates found in the document.")
    else:
        print("Failed to extract text from the PDF.")

    

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_pdf>")
    else:
        main(sys.argv[1])
