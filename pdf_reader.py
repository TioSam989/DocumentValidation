"""
Module: pdf_reader.py
Handles reading and extracting text from PDFs.
"""

import PyPDF2
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

class PDFReader:
    """
    Reads and extracts text from PDFs using PyPDF2, pdfminer, and pytesseract (for OCR).
    """

    @staticmethod
    def extract_text_pypdf2(file_path: str) -> str:
        """Extracts text using PyPDF2."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return ''.join(page.extract_text() for page in reader.pages)
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
            return ""

    @staticmethod
    def extract_text_pdfminer(file_path: str) -> str:
        """Extracts text using pdfminer."""
        try:
            return extract_text(file_path)
        except Exception as e:
            print(f"Error extracting text with pdfminer: {e}")
            return ""

    @staticmethod
    def extract_text_with_ocr(file_path: str) -> str:
        """Extracts text from image-based PDFs using OCR."""
        try:
            images = convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error performing OCR on PDF: {e}")
            return ""
