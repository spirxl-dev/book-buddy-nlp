import uvicorn
from fastapi import FastAPI

from config import SPACY_MODEL_NAME
from src.utils.utilities import install_spacy_model
from api.routers import extract_entities


def create_app() -> FastAPI:
    install_spacy_model(SPACY_MODEL_NAME)

    app = FastAPI()
    app.include_router(extract_entities.router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="localhost", port=8000, reload=True)


# def main():
#     """Runs book buddy from the CLI"""
#     install_spacy_model(SPACY_MODEL_NAME)

#     intent_recogniser = IntentRecogniser(GENRES, SPACY_MODEL_NAME)
#     recommendation_engine = RecommendationEngine("data/books.json")

#     cli_handler = CLIHandler(intent_recogniser, recommendation_engine)
#     cli_handler.run()
