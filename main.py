"""
main.py
Versão 'worker' sem menus interativos.
"""

import sys
import os
import json
import requests  # Added for making API requests
from src.utils.extract_text import extract_images_from_pdf, extract_text_from_image
from src.utils.utils import clear_console, save_images
from date_validator import DateValidator
from pdf_reader import PDFReader

# Load environment variables
from dotenv import load_dotenv

load_dotenv()  # Loads variables from a .env file if present

# Define API endpoints from environment variables
API_ROUTE_INVALID_DATES = os.getenv('API_ROUTE_INVALID_DATES')
API_ROUTE_NO_DATES = os.getenv('API_ROUTE_NO_DATES')
API_ROUTE_VALID_DATES = os.getenv('API_ROUTE_VALID_DATES')

# Optional: Configure logging
import logging

logging.basicConfig(
    filename='validation.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def detect_file_type(path_or_url: str) -> str:
    """
    Detecta se a extensão do arquivo é PDF ou imagem.
    """
    _, ext = os.path.splitext(path_or_url.lower())
    if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        return "image"
    elif ext == ".pdf":
        return "pdf"
    else:
        return "unknown"

def process_file(path_or_url: str) -> str:
    """
    Processa um arquivo PDF ou imagem (local ou URL), retornando texto extraído.
    """
    # Verifica se é local ou URL
    is_url = path_or_url.startswith("http")

    # Detecta se é PDF ou imagem
    ftype = detect_file_type(path_or_url)

    if ftype == "image":
        # Chama a função para extrair texto de imagem
        text = extract_text_from_image(path_or_url, use_local_image=not is_url) or ""
        logging.info(f"Extracted text from image: {path_or_url}")
        return text
    elif ftype == "pdf":
        # Se for PDF, extrai as páginas como imagens
        images = extract_images_from_pdf(path_or_url, use_local=not is_url)
        if images:
            texts = []
            for img in images:
                txt = extract_text_from_image(img, use_local_image=True)
                if txt:
                    texts.append(txt)
            combined_text = "\n".join(texts)
            logging.info(f"Extracted text from PDF: {path_or_url}")
            return combined_text
        else:
            logging.warning(f"No images extracted from PDF: {path_or_url}")
            return ""
    else:
        logging.warning(f"Unknown file type: {path_or_url}")
        return ""

def extract_dates(text: str) -> tuple:
    """
    Extrai todas as possíveis datas e valida quais são corretas.
    Retorna uma tupla (possible_dates, valid_dates).
    """
    possible_dates = DateValidator.find_dates(text)
    valid_dates = [d for d in possible_dates if DateValidator.validate_date(d)]
    logging.info(f"Possible dates found: {possible_dates}")
    logging.info(f"Valid dates found: {valid_dates}")
    return possible_dates, valid_dates

def call_api(route: str, payload: dict):
    """
    Faz uma requisição POST para a API especificada com o payload fornecido.
    Retorna uma resposta JSON.
    """
    try:
        response = requests.post(route, json=payload)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
        logging.info(f"Successfully called {route} with payload: {payload}")
        return {
            "status": "success",
            "route": route,
            "response": response.json() if response.content else {}
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao chamar {route}: {e}")
        return {
            "status": "error",
            "route": route,
            "message": str(e)
        }

def main():
    """
    Modo de execução CLI:
    python main.py <caminho-ou-URL>
    """
    if len(sys.argv) < 2:
        error_message = "Uso: python main.py <path_or_url_do_arquivo>"
        print(json.dumps({"status": "error", "message": error_message}))
        logging.error(error_message)
        sys.exit(1)

    path_or_url = sys.argv[1]
    logging.info(f"Processing file: {path_or_url}")

    # 1) Extrai o texto
    extracted_text = process_file(path_or_url)
    if not extracted_text:
        no_text_message = "Nenhum texto foi extraído."
        print(json.dumps({"status": "no_text", "message": no_text_message}))
        logging.warning(no_text_message)
        sys.exit(0)

    # Optional: Print a preview of the extracted text (can be removed if not needed)
    preview = extracted_text[:500]
    print("\n=== Texto Extraído ===\n")
    print(preview)
    print("\n======================\n")
    logging.info(f"Extracted text preview: {preview}")

    # 2) (Opcional) Extrair datas
    possible_dates, valid_dates = extract_dates(extracted_text)

    if valid_dates:
        print("Datas válidas encontradas:")
        for date_str in valid_dates:
            print(f"  - {date_str}")
        # Chama API Route 3
        payload = {
            "file": path_or_url,
            "valid_dates": valid_dates
        }
        api_response = call_api(API_ROUTE_VALID_DATES, payload)
        # Output for Laravel
        output = {
            "status": "valid",
            "valid_dates": valid_dates,
            "api_response": api_response
        }
        print(json.dumps(output))
    elif possible_dates:
        print("Datas encontradas, mas nenhuma é válida.")
        for date_str in possible_dates:
            print(f"  - {date_str}")
        # Chama API Route 1
        payload = {
            "file": path_or_url,
            "invalid_dates": possible_dates
        }
        api_response = call_api(API_ROUTE_INVALID_DATES, payload)
        # Output for Laravel
        output = {
            "status": "invalid",
            "invalid_dates": possible_dates,
            "api_response": api_response
        }
        print(json.dumps(output))
    else:
        print("Nenhuma data encontrada.")
        # Chama API Route 2
        payload = {
            "file": path_or_url,
            "message": "Nenhuma data encontrada no documento."
        }
        api_response = call_api(API_ROUTE_NO_DATES, payload)
        # Output for Laravel
        output = {
            "status": "no_dates",
            "message": "Nenhuma data encontrada no documento.",
            "api_response": api_response
        }
        print(json.dumps(output))

if __name__ == "__main__":
    main()
