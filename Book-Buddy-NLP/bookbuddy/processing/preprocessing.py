from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import contractions

# import nltk
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('stopwords')


def expand_contractions(text: str) -> str:
    return contractions.fix(text)


def strip_punctuation(text: str) -> str:
    chars_to_remove = ".,':;!?\""
    translation_table = text.maketrans("", "", chars_to_remove)
    out = text.translate(translation_table)
    return out


def normalise_case(text: str) -> str:
    return text.lower()


def tokenize_text(text: str) -> list:
    return word_tokenize(text)


def remove_stop_words(tokens: list) -> list:
    preserve_words = set(["not"])
    stopwords_set = set(stopwords.words("english")) - preserve_words
    return [token for token in tokens if token not in stopwords_set]


def lemmatize_tokens(tokens: list) -> list:
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def pre_process_text(text: str) -> list:
    """ENTRY POINT"""
    text = expand_contractions(text)
    text = strip_punctuation(text)
    text = normalise_case(text)
    tokens = tokenize_text(text)
    tokens = remove_stop_words(tokens)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return lemmatized_tokens
