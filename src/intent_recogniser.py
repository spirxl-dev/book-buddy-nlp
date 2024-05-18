import spacy
from src.data_processer import DataProcessor


class IntentRecogniser:
    def __init__(self, genres, model_name):
        self.genres = genres
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def identify_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        return entities

    def get_query_intents(self, tokens, entities):
        intents = []
        for token in tokens:
            if token in self.genres:
                intents.append("genre_recommendation")
                break

        entity_types = {ent[1] for ent in entities}
        if "PERSON" in entity_types or "ORG" in entity_types:
            intents.append("author_query")
        if "WORK_OF_ART" in entity_types:
            intents.append("work_of_art_query")
        if "DATE" in entity_types:
            intents.append("date_query")
        if "LANGUAGE" in entity_types:
            intents.append("language_query")

        if not intents:
            intents.append("unknown")

        return intents

    def extract_intent_details(self, tokens: list, entities: list, detail_type: str):
        details = set()
        if detail_type == "genres":
            for token in tokens:
                if token in self.genres:
                    details.add(token)
        elif detail_type == "author":
            for entity in entities:
                if entity[1] == "PERSON":
                    details.add(entity[0])
        elif detail_type == "work_of_art":
            for entity in entities:
                if entity[1] == "WORK_OF_ART":
                    details.add(entity[0])
        elif detail_type == "date":
            for entity in entities:
                if entity[1] == "DATE":
                    details.add(entity[0])
        elif detail_type == "language":
            for entity in entities:
                if entity[1] == "LANGUAGE":
                    details.add(entity[0])
        return details

    def process_query(self, input_string):
        """
        ENTRY POINT: Processes the input query to extract intents and relevant details.
        """
        tokens = DataProcessor.process_text(input_string, self.nlp)
        entities = self.identify_entities(input_string)
        intents = self.get_query_intents(tokens, entities)

        details = {
            "genres": set(),
            "authors": set(),
            "works_of_art": set(),
            "dates": set(),
            "language": set(),
        }
        for intent in intents:
            if intent == "genre_recommendation":
                details["genres"].update(
                    self.extract_intent_details(tokens, entities, "genres")
                )
            elif intent == "author_query":
                details["authors"].update(
                    self.extract_intent_details(tokens, entities, "author")
                )
            elif intent == "work_of_art_query":
                details["works_of_art"].update(
                    self.extract_intent_details(tokens, entities, "work_of_art")
                )
            elif intent == "date_query":
                details["dates"].update(
                    self.extract_intent_details(tokens, entities, "date")
                )
            elif intent == "language_query":
                details["language"].update(
                    self.extract_intent_details(tokens, entities, "language")
                )

        return entities, intents, details
