import json
import subprocess
import sys

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import contractions
from spellchecker import SpellChecker
import spacy


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
    def check_spelling(tokens):
        spell = SpellChecker()
        corrected_tokens = []
        for token in tokens:
            corrected_tokens.append(spell.correction(token))
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
    def lemmatize_tokens(tokens):
        lemmatizer = WordNetLemmatizer()
        result = []
        for token in tokens:
            lemmatized_token = lemmatizer.lemmatize(token)
            result.append(lemmatized_token)
        return result

    @staticmethod
    def process_text(text):
        text = DataProcessor.expand_contractions(text)
        text = DataProcessor.strip_punctuation(text)
        text = DataProcessor.normalise_case(text)
        tokens = DataProcessor.tokenize_text(text)
        tokens = DataProcessor.check_spelling(tokens)
        tokens = DataProcessor.remove_stop_words(tokens)
        return DataProcessor.lemmatize_tokens(tokens)


class IntentRecogniser:
    def __init__(self, genres, model_name):
        self.genres = genres
        self.model_name = model_name
        self.nlp = spacy.load(self.model_name)

    def classify_intent(self, preprocessed_tokens):
        for token in preprocessed_tokens:
            if token in self.genres:
                return "genre_recommendation"
        return "unknown"

    def extract_details(self, preprocessed_tokens, detail_type="genres"):
        details = set()
        if detail_type == "genres":
            for token in preprocessed_tokens:
                if token in self.genres:
                    details.add(token)
        return details

    def extract_intent(self, input_string):
        preprocessed_tokens = DataProcessor.process_text(input_string)
        intent = self.classify_intent(preprocessed_tokens)
        details = self.extract_details(preprocessed_tokens, detail_type="genres")
        return intent, details


class CLIHandler:
    def __init__(self, intent_recogniser):
        self.intent_recogniser = intent_recogniser

    def display_welcome_message(self):
        print("Welcome to Book-Buddy. Please enter your query. ")

    def get_user_input(self):
        return input("Your query: ")

    def display_intent_and_details(self, intent, details):
        print(f"Identified Intent: {intent}")
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
    SPACY_MODEL_NAME = "en_core_web_sm"
    install_spacy_model(SPACY_MODEL_NAME)

    GENRES = DataProcessor.load_data_from_json("data/genres.json")
    intent_recognizer = IntentRecogniser(GENRES, SPACY_MODEL_NAME)
    cli = CLIHandler(intent_recognizer)
    cli.run()


if __name__ == "__main__":
    main()
