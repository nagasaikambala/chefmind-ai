import json
import os

def load_recipes():
    # Correct path: project_root/recipes.json
    root = os.path.dirname(os.path.dirname(__file__))  # go up to project folder
    file_path = os.path.join(root, "recipes.json")

    print("Loading recipes from:", file_path)  # Debug

    with open(file_path, "r") as f:
        data = json.load(f)

    print("Loaded recipes:", len(data))  # Debug
    return data
