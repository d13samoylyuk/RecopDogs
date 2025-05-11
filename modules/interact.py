from time import sleep
from modules.basic_functions import clear_terminal


def ask(ask_text='', lower=False):
    response = input(ask_text).strip()
    if lower:
        response = response.lower()
    return response


def show_screen(interact_text, clear_firts=True, smooth_in=False):
    main_screen = '''
 -- RecopDogs: breeds photos uploader --

{interact_text}'''

    if clear_firts:
        clear_terminal()
    text = main_screen.format(interact_text=interact_text)
    if smooth_in:
        for line in text.split('\n'):
            print(line)
            sleep(0.03)
    else:
        print(text)