import spacy


class EntityRecogniser:
    def __init__(self, genres, model_name):
        self.genres = genres
        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def identify_entities(self, text) -> list:
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({"entity": ent.text, "type": ent.label_})
        return entities
