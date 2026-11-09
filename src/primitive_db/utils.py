import json
import os

from .constants import DATA_DIR


def load_metadata(filepath):
    try:
        with open(filepath) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def load_table_data(table_name):
    try:
        with open(f"data/{table_name}.json") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_metadata(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file)

def save_table_data(table_name, data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(f"data/{table_name}.json", "w") as file:
        json.dump(data, file)