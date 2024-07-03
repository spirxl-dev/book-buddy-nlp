from fastapi import HTTPException
from api.models.request.request_models import QueryRequest
from api.models.response.response_models import EntitiesQueryResponse
from src.services.entity_recogniser import EntityRecogniser
from src.config import SPACY_MODEL_NAME, GENRES

entity_recogniser = EntityRecogniser(GENRES, SPACY_MODEL_NAME)


def extract_entities_logic(request: QueryRequest) -> EntitiesQueryResponse:
    try:
        entities = entity_recogniser.return_entities(request.input_string)
        return EntitiesQueryResponse(entities=entities)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
