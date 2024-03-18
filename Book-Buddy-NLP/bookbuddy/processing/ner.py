# This module uses Named Entity Recognition (NER) to identify and extract entities like authors, genres, or themes from text.
from preprocessing import process_text
from intent import extract_intent
from pprint import pprint

input_string = "Give me a science fiction book by frank herbert"
proccessed_text = process_text(input_string)
identified_intent, details = extract_intent(input_string)
pprint(f"Identified Intent: {identified_intent}")
pprint(f"Details (Genres): {details}")
pprint(f"Identified Author: ")