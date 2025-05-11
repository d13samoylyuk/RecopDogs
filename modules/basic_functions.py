import json
import os


def clear_terminal():
    os.system('cls')


def read_json_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as j_file:
        return json.load(j_file)


def save_json_file(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as j_file:
        json.dump(data, j_file, ensure_ascii=False, indent=4)