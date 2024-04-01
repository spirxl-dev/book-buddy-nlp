import json
import subprocess
import sys
from config import SPACY_MODEL_NAME

import spacy
import contractions
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker


def install_spacy_model(model_name):
    try:
        spacy.load(model_name)
    except OSError:
        print(f"{model_name} model not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])


class DataProcessor:
    @staticmethod
    def load_data_from_json(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    @staticmethod
    def expand_contractions(text):
        return contractions.fix(text)

    @staticmethod
    def strip_punctuation(text):
        chars_to_remove = ".,':;!?\""
        translation_table = str.maketrans("", "", chars_to_remove)
        return text.translate(translation_table)

    @staticmethod
    def normalise_case(text):
        return text.lower()

    @staticmethod
    def tokenize_text(text):
        return word_tokenize(text)

    @staticmethod
    def extract_named_entities(text, nlp):
        doc = nlp(text)
        entities = set()
        names = set()

        for ent in doc.ents:
            entities.add(ent.text)
            if ent.label_ == "PERSON":
                names.add(ent.text)

        if names:
            return entities
        else:
            return ""

    @staticmethod
    def check_spelling(tokens, entities):
        spell = SpellChecker()
        corrected_tokens = []

        normalized_entities = set()
        for entity in entities:
            for word in entity.lower().split():
                normalized_entities.add(word)

        for token in tokens:
            if token.lower() not in normalized_entities:
                corrected_token = spell.correction(token)
                corrected_tokens.append(corrected_token)
            else:
                corrected_tokens.append(token)

        return corrected_tokens

    @staticmethod
    def remove_stop_words(tokens):
        preserve_words = {"not"}
        stopwords_set = set(stopwords.words("english")) - preserve_words
        result = []
        for token in tokens:
            if token not in stopwords_set:
                result.append(token)
        return result

    @staticmethod
    def lemmatize_tokens(tokens, nlp):
        doc = nlp(" ".join(tokens))
        lemmatized_tokens = []
        for token in doc:
            lemmatized_tokens.append(token.lemma_)
        return lemmatized_tokens

    @classmethod
    def process_text(cls, text, nlp):
        print("\n[INFO] Raw Text: ", text)

        entities = cls.extract_named_entities(text, nlp)
        print("[INFO] Named Entities: ", entities)

        text = cls.expand_contractions(text)
        print("[INFO] Expanded Contractions: ", text)

        text = cls.strip_punctuation(text)
        print("[INFO] Stripped Punctuation: ", text)

        text = cls.normalise_case(text)
        print("[INFO] Normalised case: ", text)

        tokens = cls.tokenize_text(text)
        print("[INFO] Tokenized: ", tokens)

        tokens = cls.check_spelling(tokens, entities)
        print("[INFO] Spelling checked: ", tokens)

        tokens = cls.remove_stop_words(tokens)
        print("[INFO] Stop words removed: ", tokens)

        tokens = cls.lemmatize_tokens(tokens, nlp)
        print("[INFO] Tokens lemmatized: ", tokens)

        return tokens


class IntentRecogniser:
    def __init__(self, genres, authors, model_name):
        self.genres = genres
        self.authors = authors
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def classify_intent(self, preprocessed_tokens, named_entities=None):
        for token in preprocessed_tokens:
            if token in self.genres:
                return "genre_recommendation"
        if named_entities:
            for entity in named_entities:
                if entity[1] in {"PERSON", "ORG"}:
                    return "author_query"
        return "unknown"

    def extract_details(
        self, preprocessed_tokens, named_entities=None, detail_type="genres"
    ):
        details = set()
        if detail_type == "genres":
            for token in preprocessed_tokens:
                if token in self.genres:
                    details.add(token)
        if named_entities and detail_type == "author":
            for entity in named_entities:
                if entity[1] == "PERSON":
                    details.add(entity[0])
        return details

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        return entities

    def extract_intent(self, input_string):
        preprocessed_tokens = DataProcessor.process_text(input_string, self.nlp)
        named_entities = self.extract_entities(input_string)
        intent = self.classify_intent(preprocessed_tokens, named_entities)
        if intent == "genre_recommendation":
            detail_type = "genres"
        else:
            detail_type = "author"
        details = self.extract_details(preprocessed_tokens, named_entities, detail_type)
        return intent, details


class CLIHandler:
    def __init__(self, intent_recogniser):
        self.intent_recogniser = intent_recogniser

    def display_welcome_message(self):
        print("\nWelcome to Book-Buddy. Please enter your query. ")

    def get_user_input(self):
        return input("\nYour query: ")

    def display_intent_and_details(self, intent, details):
        print(f"\nIdentified Intent: {intent}")
        print(f"Details (Genres): {details}")

    def run(self):
        self.display_welcome_message()
        try:
            while True:
                user_input = self.get_user_input()
                intent, details = self.intent_recogniser.extract_intent(user_input)
                self.display_intent_and_details(intent, details)
        except KeyboardInterrupt:
            print("\nExiting Book-Buddy. Goodbye!")


def main():
    GENRES = DataProcessor.load_data_from_json("data/genres.json")
    AUTHORS = DataProcessor.load_data_from_json("data/authors.json")

    install_spacy_model(SPACY_MODEL_NAME)

    intent_recognizer = IntentRecogniser(
        genres=GENRES, authors=AUTHORS, model_name=SPACY_MODEL_NAME
    )

    cli = CLIHandler(intent_recognizer)
    cli.run()


if __name__ == "__main__":
    main()
