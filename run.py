from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from config import SPACY_MODEL_NAME
from src.utils.utilities import install_spacy_model, load_json_data


def main():
    install_spacy_model(SPACY_MODEL_NAME)

    genres = load_json_data("data/genres.json")

    intent_recogniser = IntentRecogniser(genres, SPACY_MODEL_NAME)


    cli_handler = CLIHandler(intent_recogniser)
    cli_handler.run()


if __name__ == "__main__":
    main()
