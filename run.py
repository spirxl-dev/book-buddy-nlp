from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from src.aggregators.google_books_aggregator import GoogleBooksAggregator
from config import SPACY_MODEL_NAME, GOOGLE_BOOKS_API_KEY
from src.utils.utilities import install_spacy_model, load_json_data


def main_aggregator():

    aggregator = GoogleBooksAggregator(
        api_key=GOOGLE_BOOKS_API_KEY, genres_path="data/api_test_genres.json"
    )

    aggregator.download_and_save_books(output_path="data/6_books.json")

    # aggregator.download_and_save_authors(output_path="data/5_authors.json")


def main_run_cli():
    install_spacy_model(SPACY_MODEL_NAME)

    genres = load_json_data("data/genres.json")

    intent_recogniser = IntentRecogniser(genres, SPACY_MODEL_NAME)

    cli_handler = CLIHandler(intent_recogniser)
    cli_handler.run()


if __name__ == "__main__":
    main_aggregator()
