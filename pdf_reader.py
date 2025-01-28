"""
pdf_reader.py
Módulo para extrair texto de PDF usando PyPDF2, pdfminer ou OCR como fallback.
"""
import PyPDF2
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

class PDFReader:
    @staticmethod
    def extract_text_pypdf2(file_path: str) -> str:
        """Extracts text using PyPDF2."""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return "".join(page.extract_text() for page in reader.pages)
        except:
            return ""

    @staticmethod
    def extract_text_pdfminer(file_path: str) -> str:
        """Extracts text using pdfminer."""
        try:
            return extract_text(file_path)
        except:
            return ""

    @staticmethod
    def extract_text_with_ocr(file_path: str) -> str:
        """Extracts text from image-based PDFs (OCR)."""
        try:
            images = convert_from_path(file_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img)
            return text
        except:
            return ""
