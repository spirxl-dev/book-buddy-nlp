from pydantic import BaseModel
from typing import List, Dict, Any


class EntitiesQueryResponse(BaseModel):
    entities: List[Any]


class BookRecommendationResponse(BaseModel):
    intents: List[Any]
    entities: List[Any]
