import uvicorn
from fastapi import FastAPI

from src.config import SPACY_MODEL_NAME
from src.services.utils.utilities import install_spacy_model
from api.routers import extract_entities, recommend_books




if __name__ == "__main__":
    main()
