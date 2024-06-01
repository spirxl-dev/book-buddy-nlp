from pydantic import BaseModel
from typing import List, Dict, Any

class QueryResponse(BaseModel):
    entities: List[Any]
    intents: List[str]
    details: Dict[str, Any]
