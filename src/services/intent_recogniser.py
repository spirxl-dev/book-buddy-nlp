class IntentRecogniser:

    def get_query_intents(self, genres, entities) -> list:
        self.genres = genres
        self.intents = []

        entity_types = {ent["type"] for ent in entities}

        # Create a custom NER label called GENRE
        for entity in entities:
            if entity["entity"].lower() in self.genres:
                self.intents.append("genre_recommendation")

        if "PERSON" in entity_types or "ORG" in entity_types:
            self.intents.append("author_query")
        if "WORK_OF_ART" in entity_types:
            self.intents.append("work_of_art_query")
        if "DATE" in entity_types:
            self.intents.append("date_query")
        if "LANGUAGE" in entity_types:
            self.intents.append("language_query")
        if "GPE" in entity_types:
            self.intents.append("location_query")
        if "LOC" in entity_types:
            self.intents.append("location_query")
        if "NORP" in entity_types:
            self.intents.append("group_query")
        if "FAC" in entity_types:
            self.intents.append("facility_query")
        if "PRODUCT" in entity_types:
            self.intents.append("product_query")
        if "EVENT" in entity_types:
            self.intents.append("event_query")
        if "LAW" in entity_types:
            self.intents.append("law_query")
        if "LANGUAGE" in entity_types:
            self.intents.append("language_query")
        if "PERCENT" in entity_types:
            self.intents.append("percent_query")
        if "MONEY" in entity_types:
            self.intents.append("money_query")
        if "QUANTITY" in entity_types:
            self.intents.append("quantity_query")
        if "ORDINAL" in entity_types:
            self.intents.append("ordinal_query")
        if "CARDINAL" in entity_types:
            self.intents.append("cardinal_query")
        if "TIME" in entity_types:
            self.intents.append("time_query")

        if not self.intents:
            self.intents.append("unknown")

        return self.intents
