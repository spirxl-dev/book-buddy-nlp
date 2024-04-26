import spacy
from src.data_processer import DataProcessor
from pprint import pprint


class IntentRecogniser:
    def __init__(self, genres, model_name):
        """
        Initializes the IntentRecogniser with a list of genres and a spaCy model.

        Args:
            genres (set): A list of genres to be used for intent recognition.
            model_name (str): The name of the spaCy model to load for processing.
        """
        self.genres = genres
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def identify_entities(self, text):
        """
        Extracts named entities from the given text using the loaded spaCy model.

        Args:
            text (str): Text from which to identify named entities.

        Returns:
            list of tuple: A list of tuples where each tuple contains an entity and its type.
        """
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        return entities

    def get_query_intents(self, tokens, entities):
        """
        Determines the intents of a query based on preprocessed tokens and named entities.

        Args:
            tokens (list of str): Preprocessed tokens from the user's input.
            entities (list of tuple): Named entities identified from the user's input.

        Returns:
            list of str: A list of identified intents such as 'genre_recommendation', 'author_query', or 'unknown'.
        """
        intents = []
        for token in tokens:
            if token in self.genres:
                intents.append("genre_recommendation")
                break

        if entities:
            for entity in entities:
                if entity[1] in {"PERSON", "ORG"}:
                    intents.append("author_query")
                    break

        if not intents:
            intents.append("unknown")

        return intents

    def extract_intent_details(self, tokens, entities, detail_type="genres"):
        """
        Extracts details relevant to the identified intents from tokens and named entities.

        Args:
            tokens (list of str): Preprocessed tokens from the user's input.
            entities (list of tuple): Named entities identified from the user's input.
            detail_type (str): Type of detail to extract, either 'genres' or 'author'.

        Returns:
            set: Details corresponding to the specified detail type.
        """
        details = set()
        if detail_type == "genres":
            for token in tokens:
                if token in self.genres:
                    details.add(token)
        elif detail_type == "author" and entities:
            for entity in entities:
                if entity[1] == "PERSON":
                    details.add(entity[0])
        return details

    def process_query(self, input_string):
        """
        ENTRY POINT: Processes the input query to extract intents and relevant details.

        Args:
            input_string (str): User input string to be processed.

        Returns:
            tuple: A tuple containing the named entities, identified intents, and details related to each intent.
        """
        tokens = DataProcessor.process_text(input_string, self.nlp)
        entities = self.identify_entities(input_string)
        intents = self.get_query_intents(tokens, entities)

        details = {"genres": set(), "authors": set()}
        for intent in intents:
            if intent == "genre_recommendation":
                details["genres"].update(
                    self.extract_intent_details(tokens, entities, "genres")
                )
            elif intent == "author_query":
                details["authors"].update(
                    self.extract_intent_details(tokens, entities, "author")
                )

        return entities, intents, details
