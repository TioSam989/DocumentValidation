import os
import time
from PIL import ImageOps,ImageChops, Image

def get_word_count(file_path='./output.txt'):
    return int(os.popen(f"cat {file_path} | wc -w").read().strip())

def get_char_count(file_path='./output.txt'): 
    return int(os.popen(f"cat {file_path} | wc -c").read().strip())

def clear_console(wait_time=None):
    if wait_time is not None:
        sleep(wait_time)
    os.system("cls" if os.name == "nt" else "clear")

def sleep(seconds):
    time.sleep(seconds)

def is_local_file(path_or_url):
    return os.path.isfile(path_or_url)

def save_images(imgs):
    
    temp_folder = create_temp_folder()
    
    for idx, img in enumerate(imgs):
        image_path = os.path.join(temp_folder, f"page_{time.strftime('%Y-%m-%d-%H-%M-%S-%f')}.png")
        img.save(image_path)

def convert_to_grayscale(img):
    return ImageOps.grayscale(img)

def increase_contrast(img):
    return ImageOps.autocontrast(img)

def binarize_image(img):
    return img.convert("L").point(lambda x: 0 if x < 128 else 255, mode="1")

def preprocess_image(img):
    img = convert_to_grayscale(img)
    img = increase_contrast(img)
    img = binarize_image(img)
    return img

def create_temp_folder(folder_name="temp_images"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)