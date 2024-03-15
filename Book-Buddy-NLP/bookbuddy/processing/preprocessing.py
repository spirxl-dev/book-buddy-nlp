# This module is responsible for text normalization and preprocessing to prepare user queries for NLP analysis.
import re
from nltk.corpus import stopwords
import contractions


def normalise_case(text: str):
    out = text.lower()
    return out


def remove_punctuation_and_special_chars(text: str):
    # out = text.translate(str.maketrans("", "", string.punctuation))
    out = re.sub("[^a-zA-Z\s]", "", text)
    return out


def remove_stop_words(text: str):
    stopwords_dict = {word: 1 for word in stopwords.words("english")}
    words = []
    for word in text.split():
        if word.lower() not in stopwords_dict:
            words.append(word)
    text = " ".join(words)
    return text


def expand_contractions(text: str):
    """Potentially a bit iffy"""
    out = contractions.fix(text)
    return out

print(expand_contractions("yall shouldnt shit"))


def lemmatization(text: str):
    pass


def pre_proccess_text(text: str):
    """ENTRY POINT"""
    pass
