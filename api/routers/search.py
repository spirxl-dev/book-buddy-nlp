from fastapi import APIRouter, HTTPException
from api.models.request.request_models import QueryRequest
from api.models.response.response_models import QueryResponse
from src.intent_recogniser import IntentRecogniser
from config import SPACY_MODEL_NAME, GENRES


intent_recogniser = IntentRecogniser(GENRES, SPACY_MODEL_NAME)

router = APIRouter()


@router.post("/search", response_model=QueryResponse)
async def search_books(request: QueryRequest):
    try:
        entities, intents, details = intent_recogniser.process_query(
            request.input_string
        )
        return QueryResponse(entities=entities, intents=intents, details=details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
