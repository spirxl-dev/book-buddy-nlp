class IntentRecogniser:

    def get_query_intents(self, genres, entities) -> list:
        self.genres = genres
        self.intents = []

        entity_types = {ent["type"] for ent in entities}

        for entity in entities:
            if entity["entity"].lower() in self.genres:
                self.intents.append("genre_recommendation")
                break

        if "PERSON" in entity_types or "ORG" in entity_types:
            self.intents.append("author_query")
        if "WORK_OF_ART" in entity_types:
            self.intents.append("work_of_art_query")
        if "DATE" in entity_types:
            self.intents.append("date_query")
        if "LANGUAGE" in entity_types:
            self.intents.append("language_query")

        if not self.intents:
            self.intents.append("unknown")

        return self.intents
