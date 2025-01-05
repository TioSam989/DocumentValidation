import requests
import pytesseract
from io import BytesIO
from PIL import Image
import fitz
from utils.utils import preprocess_image, save_images, trim

from PIL import Image
import fitz  # PyMuPDF
import requests
from io import BytesIO

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
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = trim(img)
            images.append(img)

        pdf_document.close()
        save_images(images)  # Save images if needed
        return images

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def extract_text_from_image(image_path_or_url, use_local_image=False):
    try:
        if use_local_image:
            if isinstance(image_path_or_url, Image.Image):
                image = image_path_or_url
            else:
                image = Image.open(image_path_or_url)
        else:
            response = requests.get(image_path_or_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

        processed_image = preprocess_image(image)

        extracted_text = pytesseract.image_to_string(image, lang="por")
        return extracted_text

    except Exception as e:
        print(f"Error processing image: {e}")
        return None