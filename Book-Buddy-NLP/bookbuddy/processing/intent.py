# intent.py

from pprint import pprint
from preprocessing import process_text
from utils.utils import load_data_from_json
import spacy
import sys

sys.path.append("...")


GENRES: list = load_data_from_json("Book-Buddy-NLP/data/genres.json")
AUTHORS: list = []

nlp = spacy.load("en_core_web_sm")


def classify_intent(preprocessed_tokens: list) -> str:
    for token in preprocessed_tokens:
        if token in GENRES:
            return "genre_recommendation"
        #  Add support for authors
    return "unknown"


def extract_details(preprocessed_tokens: list, detail_type: str = "genres") -> set:
    details = set()
    if detail_type == "genres":
        for token in preprocessed_tokens:
            if token in GENRES:
                details.add(token)
    return details


def extract_intent(input_string: str) -> tuple[str, set]:
    """ENTRY POINT"""
    preprocessed_tokens = process_text(input_string)
    intent = classify_intent(preprocessed_tokens)
    details = extract_details(preprocessed_tokens, detail_type="genres")
    return intent, details


if __name__ == "__main__":
    input_string = "I'm looking for a sci-fi book with elements of romance and comedy."
    identified_intent, details = extract_intent(input_string)
    print(f"Identified Intent: {identified_intent}")
    print(f"Details (Genres): {details}")
    print
