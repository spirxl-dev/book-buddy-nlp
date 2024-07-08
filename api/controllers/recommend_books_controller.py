from api.models.request.request_models import QueryRequest
from api.models.response.response_models import BookRecommendationResponse
from src.services.book_recommender import BookRecommender
from src.services.intent_recogniser import IntentRecogniser
from src.services.entity_recogniser import EntityRecogniser
from src.config import SPACY_MODEL_NAME, GENRES




def recommend_books_logic(request: QueryRequest) -> BookRecommendationResponse:

    entity_recogniser = EntityRecogniser(GENRES, SPACY_MODEL_NAME)
    entities = entity_recogniser.return_entities(request.input_string)

    intents = IntentRecogniser().get_query_intents(entities=entities, genres=GENRES)
    
    book_recommender = BookRecommender(json_file_path="data/books.json")
    return BookRecommendationResponse(intents=intents, entities=entities)
