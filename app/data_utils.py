import json
import os

def load_recipes():
    root = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(root, "recipes.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"recipes.json not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data