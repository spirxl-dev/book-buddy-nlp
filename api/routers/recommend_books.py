from fastapi import APIRouter

from api.models.request.request_models import QueryRequest
from api.models.response.response_models import BookRecommendationResponse

from api.controllers.recommend_books_controller import recommend_books_logic

router = APIRouter()


@router.post("/recommend-books", response_model=BookRecommendationResponse)
async def recommend_books(request: QueryRequest):
    return recommend_books_logic(request)
