"""
main.py
Versão 'worker' sem menus interativos.
"""

import sys
import os
import requests  # Added for making API requests
from src.utils.extract_text import extract_images_from_pdf, extract_text_from_image
from src.utils.utils import clear_console, save_images
from date_validator import DateValidator
from pdf_reader import PDFReader

# Define API endpoints
# Get API routes from environment variables
API_ROUTES_INVALID_DATES = os.getenv('API_ROUTES_INVALID_DATES')
API_ROUTES_NO_DATES = os.getenv('API_ROUTES_NO_DATES') 
API_ROUTES_VALID_DATES = os.getenv('API_ROUTES_VALID_DATES')

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
        return extract_text_from_image(path_or_url, use_local_image=not is_url) or ""
    elif ftype == "pdf":
        # Se for PDF, extrai as páginas como imagens
        images = extract_images_from_pdf(path_or_url, use_local=not is_url)
        if images:
            texts = []
            for img in images:
                txt = extract_text_from_image(img, use_local_image=True)
                if txt:
                    texts.append(txt)
            return "\n".join(texts)
        else:
            return ""
    else:
        return ""

def extract_dates(text: str) -> tuple:
    """
    Extrai todas as possíveis datas e valida quais são corretas.
    Retorna uma tupla (possible_dates, valid_dates).
    """
    possible_dates = DateValidator.find_dates(text)
    valid_dates = [d for d in possible_dates if DateValidator.validate_date(d)]
    return possible_dates, valid_dates

def call_api(route: str, payload: dict):
    """
    Faz uma requisição POST para a API especificada com o payload fornecido.
    """
    try:
        response = requests.post(route, json=payload)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
        print(f"Successfully called {route}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar {route}: {e}")

def main():
    """
    Modo de execução CLI:
    python main.py <caminho-ou-URL>
    """
    if len(sys.argv) < 2:
        print("Uso: python main.py <path_or_url_do_arquivo>")
        sys.exit(1)

    path_or_url = sys.argv[1]

    # 1) Extrai o texto
    extracted_text = process_file(path_or_url)
    if not extracted_text:
        print("Nenhum texto foi extraído.")
        sys.exit(0)

    print("\n=== Texto Extraído ===\n")
    print(extracted_text[:500])  # Exibe apenas 500 chars como preview
    print("\n======================\n")

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
        call_api(API_ROUTES_VALID_DATES, payload)
    elif possible_dates:
        print("Datas encontradas, mas nenhuma é válida.")
        for date_str in possible_dates:
            print(f"  - {date_str}")
        # Chama API Route 1
        payload = {
            "file": path_or_url,
            "invalid_dates": possible_dates
        }
        call_api(API_ROUTES_INVALID_DATES, payload)
    else:
        print("Nenhuma data encontrada.")
        # Chama API Route 2
        payload = {
            "file": path_or_url,
            "message": "Nenhuma data encontrada no documento."
        }
        call_api(API_ROUTES_NO_DATES, payload)

if __name__ == "__main__":
    main()
