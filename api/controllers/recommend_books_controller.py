from fastapi import HTTPException
from api.models.request.request_models import QueryRequest
from api.models.response.response_models import EntitiesQueryResponse



def recommend_books_logic(request: QueryRequest) -> EntitiesQueryResponse:
    pass
