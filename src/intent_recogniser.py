import spacy
from src.data_processer import DataProcessor


class IntentRecogniser:
    def __init__(self, genres, model_name):
        self.genres = genres
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def determine_query_intent(self, preprocessed_tokens, named_entities):
        intents = []
        for token in preprocessed_tokens:
            if token in self.genres:
                intents.append("genre_recommendation")
                break

        if named_entities:
            for entity in named_entities:
                if entity[1] in {"PERSON", "ORG"}:
                    intents.append("author_query")
                    break

        if not intents:
            intents.append("unknown")

        return intents

    def extract_intent_details(
        self, preprocessed_tokens, named_entities, detail_type="genres"
    ):
        details = set()
        if detail_type == "genres":
            for token in preprocessed_tokens:
                if token in self.genres:
                    details.add(token)
        elif detail_type == "author" and named_entities:
            for entity in named_entities:
                if entity[1] == "PERSON":
                    details.add(entity[0])
        return details

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def extract_intent(self, input_string):
        preprocessed_tokens = DataProcessor.process_text(input_string, self.nlp)
        named_entities = self.extract_entities(input_string)
        intents = self.determine_query_intent(preprocessed_tokens, named_entities)

        details = {"genres": set(), "authors": set()}
        for intent in intents:
            if intent == "genre_recommendation":
                details["genres"].update(
                    self.extract_intent_details(
                        preprocessed_tokens, named_entities, "genres"
                    )
                )
            elif intent == "author_query":
                details["authors"].update(
                    self.extract_intent_details(
                        preprocessed_tokens, named_entities, "author"
                    )
                )

        return named_entities, intents, details
