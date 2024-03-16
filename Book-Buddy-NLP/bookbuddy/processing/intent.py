# intent.py

from pprint import pprint
from preprocessing import process_text
from utils.utils import load_data_from_json
import spacy
import sys

sys.path.append("...")


GENRES = load_data_from_json("Book-Buddy-NLP/data/genres.json")

nlp = spacy.load("en_core_web_sm")


def classify_intent(preprocessed_tokens: list) -> str:
    if any(token in GENRES for token in preprocessed_tokens):
        return "genre_recommendation"  #  add support for author etc.
    else:
        return "unknown"


def extract_details(preprocessed_tokens: list, detail_type: str = "genres") -> set:
    details = set()
    if detail_type == "genres":
        for token in preprocessed_tokens:
            if token in GENRES:
                details.add(token)
    return details


def process_user_request(input_string: str) -> tuple[str, set]:
    """ENTRY POINT"""
    preprocessed_tokens = process_text(input_string)
    intent = classify_intent(preprocessed_tokens)
    details = extract_details(preprocessed_tokens, detail_type="genres")
    return intent, details


if __name__ == "__main__":
    input_string = "I'm looking for a sci-fi book with elements of romance and comedy."
    identified_intent, details = process_user_request(input_string)
    print(f"Identified Intent: {identified_intent}")
    print(f"Details (Genres): {details}")
