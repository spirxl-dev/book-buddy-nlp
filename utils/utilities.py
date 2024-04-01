import subprocess
import sys
import spacy

def install_spacy_model(model_name):
    try:
        spacy.load(model_name)
    except OSError:
        print(f"{model_name} model not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])

