from pydantic import BaseModel

class QueryRequest(BaseModel):
    input_string: str
