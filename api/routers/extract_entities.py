from fastapi import APIRouter, HTTPException
from api.models.request.request_models import QueryRequest
from api.models.response.response_models import EntitiesQueryResponse
from api.controllers.extract_entities_controller import extract_entities_logic

router = APIRouter()


@router.post("/extract-entities", response_model=EntitiesQueryResponse)
async def extract_entities(request: QueryRequest):
    return extract_entities_logic(request)
