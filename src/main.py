from utils.extract_text import extract_text_from_image, extract_images_from_pdf
from utils.utils import clear_console, get_char_count, get_word_count, save_images, sleep
from simple_term_menu import TerminalMenu
from urllib.parse import urlparse
import sys
import os

def detect_file_type(path_or_url):
    path = urlparse(path_or_url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        return 'image'
    elif ext == '.pdf':
        return 'pdf'
    else:
        return 'unknown'

def main():
    clear_console()

    # Menu principal
    options = ["Image (Local)", "Image (URL)", "PDF (Local)", "PDF (URL)", None]
    if os.path.exists("output.txt"):
        chars_count = get_char_count()        
        if chars_count > 0:
            options.extend(["See latest output"])
    options.extend(["Exit", None])    
    terminal_menu = TerminalMenu(options, title="Select the file type and source or exit", show_search_hint=True)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == len(options) - 1:
        print("Exiting...")
        sys.exit(0)

    option_selected = options[menu_entry_index]

    file_path_or_url = input("Enter the file path or URL: ").strip()

    if option_selected == "Image (Local)":
        text = extract_text_from_image(file_path_or_url, use_local_image=True)
    elif option_selected == "Image (URL)":
        text = extract_text_from_image(file_path_or_url, use_local_image=False)
    elif option_selected == "PDF (Local)":
        images = extract_images_from_pdf(file_path_or_url, use_local=True)
        save_images(images)  
        text = "\n".join([extract_text_from_image(img, use_local_image=True) for img in images]) if images else None
    elif option_selected == "PDF (URL)":
        images = extract_images_from_pdf(file_path_or_url, use_local=False)
        text = "\n".join([extract_text_from_image(img, use_local_image=True) for img in images]) if images else None

    if text:
        print("\nText extracted successfully")
        
        word_count = get_word_count()
        character = get_char_count()        
        
        options = ["See full output","Extract validate date",None,"Exit"]
        terminal_menu = TerminalMenu(options, title="Select an option")
        menu_entry_index = terminal_menu.show()
        
        option_selected = options[menu_entry_index]
        
        if menu_entry_index == len(options) - 1:
            print("Exiting...")
            sys.exit(0)
            
        elif option_selected == "See full output":
            clear_console()
            
            print("In development...")
            main()
            # options = ["extract validate date",None,"exit"]
            # terminal_menu = TerminalMenu(options, title="Select an option, after see content")
            # menu_entry_index = terminal_menu.show()
            
            #show here preview of all the text file
        elif option_selected == "Extract validate date":
            clear_console()
            #call the function of extract validate date
        
    else:
        print("\nFailed to extract text.")
        
        options = ["Try again", "Exit"]
        terminal_menu = TerminalMenu(options, title="Select an option")
        menu_entry_index = terminal_menu.show()
        
        if menu_entry_index == len(options) - 1:
            clear_console()
            print("Exiting...")
            sleep(2)
        else:
            clear_console()
            main()
            
            sys.exit(0)

if __name__ == "__main__":
    main()