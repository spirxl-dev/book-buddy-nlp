from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from src.recommendation_engine import RecommendationEngine
from src.aggregators.google_books_aggregator import GoogleBooksAggregator
from config import SPACY_MODEL_NAME, GOOGLE_BOOKS_API_KEY, GENRES
from src.utils.utilities import install_spacy_model, load_json_data
from pprint import pprint


def main_aggregator():

    aggregator = GoogleBooksAggregator(api_key=GOOGLE_BOOKS_API_KEY)

    aggregator.download_and_save_books(output_path="data/books.json")


def main_demo_recommendations():
    engine = RecommendationEngine("data/books.json")

    example_output_empty = {"genres": set(), "authors": set()}

    example_output_2 = {"genres": {"Literary Criticism"}, "authors": {"Lisa Zunshine"}}
    example_output_3 = {"genres": {"horror"}, "authors": {"stephen king"}}

    pprint(engine.recommend(example_output_3))


def main_run_cli():
    install_spacy_model(SPACY_MODEL_NAME)

    # What happens if a non valid json is passed?
    recommender = RecommendationEngine("data/books.json")

    intent_recogniser = IntentRecogniser(GENRES, SPACY_MODEL_NAME)

    _, _, details = intent_recogniser.process_query(
        input_string="I want to read a science book"
    )
    recommendations = recommender.recommend(details)

    print("\nRecommendations based on your input:")
    pprint(recommendations)

    # cli_handler = CLIHandler(intent_recogniser)
    # cli_handler.run()


if __name__ == "__main__":
    main_run_cli()
