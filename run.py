import os
from dotenv import load_dotenv
from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from src.data_aggregators.google_books_aggregator import GoogleBooksAggregator
from config import SPACY_MODEL_NAME
from src.utils.utilities import install_spacy_model, load_json_data

example_output_1 = {"genres": set(), "authors": set()}
example_output_2 = {"genres": {"science"}, "authors": {"isaac asimov"}}
example_output_3 = {"genres": {"romance"}, "authors": {"jane austen"}}


def populate_data_store():
    genres = load_json_data("data/genres.json")
    genres_list = []
    for genre in genres:
        query = "subject:" + genre
        genres_list.append(query)

    populator = GoogleBooksAggregator(api_key=os.getenv("GOOGLE_BOOKS_API_KEY"))
    populator.populate_datastore(genres_list)


def main_run_cli():
    install_spacy_model(SPACY_MODEL_NAME)

    genres = load_json_data("data/genres.json")

    intent_recogniser = IntentRecogniser(genres, SPACY_MODEL_NAME)

    cli_handler = CLIHandler(intent_recogniser)
    cli_handler.run()


if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    print(api_key)
    print(type(api_key))
