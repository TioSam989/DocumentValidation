"""
main.py
Versão 'worker' sem menus interativos.
"""

import sys
import os
from src.utils.extract_text import extract_images_from_pdf, extract_text_from_image
from src.utils.utils import clear_console, save_images
from date_validator import DateValidator
from pdf_reader import PDFReader

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

def extract_dates(text: str) -> list:
    """
    Exemplo de extração de datas usando seu date_validator.py
    """
    possible_dates = DateValidator.find_dates(text)
    valid_dates = [d for d in possible_dates if DateValidator.validate_date(d)]
    return valid_dates

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
    dates_found = extract_dates(extracted_text)
    if dates_found:
        print("Datas válidas encontradas:")
        for date_str in dates_found:
            print(f"  - {date_str}")
    else:
        print("Nenhuma data válida encontrada.")

if __name__ == "__main__":
    main()
