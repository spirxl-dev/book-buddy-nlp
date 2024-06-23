import spacy


class EntityRecogniser:
    def __init__(self, genres, model_name):
        self.genres = genres
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def identify_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({"entity": ent.text, "type": ent.label_})
        return entities

    def return_entities(self, input_string):
        """
        ENTRY POINT: Processes input_string to extract all entities.
        """
        entities = self.identify_entities(input_string)
        return  entities


