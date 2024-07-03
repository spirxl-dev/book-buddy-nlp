import contractions
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker


class DataProcessor:

    @staticmethod
    def expand_contractions(text):
        return contractions.fix(text)

    @staticmethod
    def strip_punctuation(text):
        chars_to_remove = ".,':;!?\""
        translation_table = str.maketrans("", "", chars_to_remove)
        return text.translate(translation_table)

    @staticmethod
    def normalise_case(text):
        return text.lower()

    @staticmethod
    def tokenize_text(text):
        return word_tokenize(text)

    @staticmethod
    def extract_named_entities(text, nlp):
        doc = nlp(text)
        entities = set()

        for ent in doc.ents:
            entities.add(ent.text)

        if entities:
            return entities
        else:
            ""

    @staticmethod
    def check_spelling(tokens, entities):
        spell = SpellChecker()
        corrected_tokens = []

        normalized_entities = set()
        for entity in entities:
            for word in entity.lower().split():
                normalized_entities.add(word)

        for token in tokens:
            if token.lower() not in normalized_entities:
                corrected_token = spell.correction(token)
                corrected_tokens.append(corrected_token)
            else:
                corrected_tokens.append(token)

        return corrected_tokens

    @staticmethod
    def remove_stop_words(tokens):
        preserve_words = {"not"}
        stopwords_set = set(stopwords.words("english")) - preserve_words
        result = []
        for token in tokens:
            if token not in stopwords_set:
                result.append(token)
        return result

    @staticmethod
    def lemmatize_tokens(tokens, nlp):
        doc = nlp(" ".join(tokens))
        lemmatized_tokens = []
        for token in doc:
            lemmatized_tokens.append(token.lemma_)
        return lemmatized_tokens

    @classmethod
    def process_text(cls, text, nlp):
        """ENTRY POINT"""
        print("\n[INFO] Raw Text: ", text)

        entities = cls.extract_named_entities(text, nlp)
        print("[INFO] Named Entities: ", entities)

        text = cls.expand_contractions(text)
        print("[INFO] Expanded Contractions: ", text)

        text = cls.strip_punctuation(text)
        print("[INFO] Stripped Punctuation: ", text)

        text = cls.normalise_case(text)
        print("[INFO] Normalised case: ", text)

        tokens = cls.tokenize_text(text)
        print("[INFO] Tokenized: ", tokens)

        tokens = cls.check_spelling(tokens, entities)
        print("[INFO] Spelling checked: ", tokens)

        tokens = cls.remove_stop_words(tokens)
        print("[INFO] Stop words removed: ", tokens)

        tokens = cls.lemmatize_tokens(tokens, nlp)
        print("[INFO] Tokens lemmatized: ", tokens)

        return tokens
