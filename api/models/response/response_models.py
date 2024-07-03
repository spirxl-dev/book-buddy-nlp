from pydantic import BaseModel
from typing import List, Dict, Any


class EntitiesQueryResponse(BaseModel):
    entities: List[Any]


class IntentsQueryResponse(BaseModel):
    intents: List[str]


class DetailsQueryResponse(BaseModel):
    details: Dict[str, Any]


class BookRecommendationResponse(BaseModel):
    pass
