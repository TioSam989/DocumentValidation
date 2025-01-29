"""
src/utils/utils.py
Funções auxiliares
"""
import os
import time
import requests
from PIL import ImageOps, ImageChops, Image

def clear_console(wait_time=None):
    if wait_time is not None:
        time.sleep(wait_time)
    os.system("cls" if os.name == "nt" else "clear")

def save_to_output(content, mode='a'):
    """
    Helper para salvar conteúdo no output.txt (caso queira logs).
    Ajuste o path se precisar.
    """
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output.txt')
    with open(output_path, mode, encoding='utf-8') as f:
        f.write(str(content) + '\n\n')

def preprocess_image(img):
    """
    Converte em grayscale, aumenta contraste, binariza
    """
    img = convert_to_grayscale(img)
    img = increase_contrast(img)
    img = binarize_image(img)
    return img

def convert_to_grayscale(img):
    return ImageOps.grayscale(img)

def increase_contrast(img):
    return ImageOps.autocontrast(img)

def binarize_image(img):
    return img.convert("L").point(lambda x: 0 if x < 128 else 255, mode="1")

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


def trim(im):
    """
    Remove espaços em branco das bordas da imagem
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def save_images(imgs):
    """
    Salva imagens numa pasta temp, se desejar
    """
    temp_folder = create_temp_folder()
    for img in imgs:
        image_path = os.path.join(temp_folder, f"page_{time.strftime('%Y-%m-%d-%H-%M-%S-%f')}.png")
        img.save(image_path)

def create_temp_folder(folder_name="temp_images"):
    """
    Cria a pasta se não existir
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name
