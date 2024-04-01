import spacy
from src.data_processer import DataProcessor


class IntentRecogniser:
    def __init__(self, genres, authors, model_name):
        self.genres = genres
        self.authors = authors
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def determine_query_intent(self, preprocessed_tokens, named_entities=None):
        for token in preprocessed_tokens:
            if token in self.genres:
                return "genre_recommendation"
        if named_entities:
            for entity in named_entities:
                if entity[1] in {"PERSON", "ORG"}:
                    return "author_query"
        return "unknown"

    def extract_intent_details(
        self, preprocessed_tokens, named_entities=None, detail_type="genres"
    ):
        details = set()
        if detail_type == "genres":
            for token in preprocessed_tokens:
                if token in self.genres:
                    details.add(token)
        if named_entities and detail_type == "author":
            for entity in named_entities:
                if entity[1] == "PERSON":
                    details.add(entity[0])
        return details

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        return entities

    def extract_intent(self, input_string):
        preprocessed_tokens = DataProcessor.process_text(input_string, self.nlp)
        named_entities = self.extract_entities(input_string)
        intent = self.determine_query_intent(preprocessed_tokens, named_entities)
        if intent == "genre_recommendation":
            detail_type = "genres"
        else:
            detail_type = "author"

        details = self.extract_intent_details(
            preprocessed_tokens, named_entities, detail_type
        )

        return named_entities, intent, details
