from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from src.recommendation_engine import RecommendationEngine
from config import SPACY_MODEL_NAME, GENRES
from src.utils.utilities import install_spacy_model


# TODO: Split books.json into seperate generes e.g fiction.json, romance.json
# TODO: Add intent recognition for WORK_OF_ART.
# TODO: Add intent recognition  for dates e.g 2008.
# TODO: Add intent recoginition for date ranges.
# TODO: Run mixed intent query tests in README.md
# TODO: End-to-end integration testing?


def main():
    install_spacy_model(SPACY_MODEL_NAME)

    intent_recogniser = IntentRecogniser(GENRES, SPACY_MODEL_NAME)
    recommendation_engine = RecommendationEngine("data/books.json")

    cli_handler = CLIHandler(intent_recogniser, recommendation_engine)
    cli_handler.run()


if __name__ == "__main__":
    main()
