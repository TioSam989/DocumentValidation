"""
src/utils/extract_text.py
Funções para extrair imagens de PDFs e extrair texto de imagens.
"""
import requests
import pytesseract
from io import BytesIO
from PIL import Image
import fitz
import os
from .utils import preprocess_image, save_to_output, trim

def extract_images_from_pdf(pdf_path_or_url, use_local=False, dpi=200):
    try:
        if use_local:
            pdf_document = fitz.open(pdf_path_or_url)
        else:
            response = requests.get(pdf_path_or_url)
            response.raise_for_status()
            pdf_data = BytesIO(response.content)
            pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        images = []
        save_to_output(f"Processing PDF: {pdf_path_or_url}")

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = trim(img)
            images.append(img)
            save_to_output(f"Extracted image from page {page_num + 1}")

        pdf_document.close()
        return images

    except Exception as e:
        error_msg = f"Error processing PDF: {e}"
        save_to_output(error_msg)
        print(error_msg)
        return None

def extract_text_from_image(image_path_or_url, use_local_image=False):
    try:
        if use_local_image:
            # Caso já seja um objeto PIL.Image:
            if isinstance(image_path_or_url, Image.Image):
                image = image_path_or_url
            else:
                image = Image.open(image_path_or_url)
        else:
            response = requests.get(image_path_or_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

        processed_image = preprocess_image(image)
        extracted_text = pytesseract.image_to_string(processed_image, lang="por")

        save_to_output(f"Extracted text from image: {image_path_or_url}")
        save_to_output(extracted_text)
        return extracted_text

    except Exception as e:
        error_msg = f"Error processing image: {e}"
        save_to_output(error_msg)
        print(error_msg)
        return None
