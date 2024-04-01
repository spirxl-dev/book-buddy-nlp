from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from src.data_processer import DataProcessor
from config import SPACY_MODEL_NAME
from utils.utilities import install_spacy_model


def main():
    install_spacy_model(SPACY_MODEL_NAME)

    data_processor = DataProcessor()
    genres = data_processor.load_json_data("data/genres.json")
    authors = data_processor.load_json_data("data/authors.json")

    intent_recognizer = IntentRecogniser(genres, authors, SPACY_MODEL_NAME)
    cli_handler = CLIHandler(intent_recognizer)

    cli_handler.run()


if __name__ == "__main__":
    main()
