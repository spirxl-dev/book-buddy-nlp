class IntentRecogniser:
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
