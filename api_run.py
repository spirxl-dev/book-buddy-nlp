import uvicorn
from fastapi import FastAPI

from src.cli_handler import CLIHandler
from src.intent_recogniser import IntentRecogniser
from src.recommendation_engine import RecommendationEngine
from config import SPACY_MODEL_NAME, GENRES
from src.utils.utilities import install_spacy_model
from api.routers import search




def main():
    """Runs book buddy from the CLI"""
    install_spacy_model(SPACY_MODEL_NAME)

    intent_recogniser = IntentRecogniser(GENRES, SPACY_MODEL_NAME)
    recommendation_engine = RecommendationEngine("data/books.json")

    cli_handler = CLIHandler(intent_recogniser, recommendation_engine)
    cli_handler.run()

def create_app() -> FastAPI:
    install_spacy_model(SPACY_MODEL_NAME)

    app = FastAPI()
    app.include_router(search.router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=False)
