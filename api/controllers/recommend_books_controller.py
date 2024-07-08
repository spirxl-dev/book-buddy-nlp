from fastapi import HTTPException
from api.models.request.request_models import QueryRequest
from api.models.response.response_models import EntitiesQueryResponse
from src.services.book_recommender import BookRecommender



def recommend_books_logic(request: QueryRequest) -> EntitiesQueryResponse:
    book_recommender = BookRecommender(json_file_path='data/books.json')
    pass
