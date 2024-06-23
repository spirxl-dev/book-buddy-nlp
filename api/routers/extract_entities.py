from fastapi import APIRouter, HTTPException
from api.models.request.request_models import QueryRequest
from api.models.response.response_models import EntitiesQueryResponse
from src.entity_recogniser import EntityRecogniser
from src.recommendation_engine import RecommendationEngine
from config import SPACY_MODEL_NAME, GENRES


entity_recogniser = EntityRecogniser(GENRES, SPACY_MODEL_NAME)

router = APIRouter()


@router.post("/extract-entities", response_model=EntitiesQueryResponse)
async def search_books(request: QueryRequest):
    try:
        entities = entity_recogniser.return_entities(request.input_string)
        return EntitiesQueryResponse(entities=entities)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
