import subprocess
import json
import sys
import spacy


def install_spacy_model(model_name):
    try:
        spacy.load(model_name)
    except OSError:
        print(f"{model_name} model not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])


def load_json_data(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_json_data(data, json_file):
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
