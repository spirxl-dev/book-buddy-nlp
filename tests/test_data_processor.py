import pytest
from unittest.mock import MagicMock
from src.data_processer import DataProcessor


@pytest.fixture
def mock_nlp(mocker):
    mock_nlp = mocker.MagicMock()
    mocker.patch("spacy.load", return_value=mock_nlp)
    return mock_nlp


@pytest.fixture
def mock_spellchecker(mocker):
    mocker.patch("src.data_processer.SpellChecker.correction", side_effect=lambda x: x)


def test_expand_contractions():
    contractions = {
        "I'm": "I am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "aren't": "are not",
        "isn't": "is not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "won't": "will not",
        "wouldn't": "would not",
        "can't": "cannot",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mightn't": "might not",
        "mustn't": "must not",
        "I've": "I have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "who's": "who is",
        "what's": "what is",
        "where's": "where is",
        "when's": "when is",
        "why's": "why is",
        "how's": "how is",
        "cant": "cannot",
        "wont": "will not",
        "dont": "do not",
    }

    for contraction, expected in contractions.items():
        assert DataProcessor.expand_contractions(contraction) == expected


def test_strip_punctuation():
    test_text = "Hello, world! Whats Up?"
    expected_text = "Hello world Whats Up"
    assert DataProcessor.strip_punctuation(test_text) == expected_text


def test_normalise_case():
    test_text = "Lowercase Text"
    expected_text = "lowercase text"
    assert DataProcessor.normalise_case(test_text) == expected_text


def test_tokenize_text():
    test_text = "This is a test."
    expected_tokens = [
        "This",
        "is",
        "a",
        "test",
        ".",
    ]
    assert DataProcessor.tokenize_text(test_text) == expected_tokens


def test_extract_named_entities(mock_nlp):
    mock_doc = MagicMock()
    mock_ent = MagicMock()
    mock_ent.text = "John Smith"
    mock_ent.label_ = "PERSON"
    mock_doc.ents = [mock_ent]

    mock_nlp.return_value = mock_doc

    text = "This is a test written by John Smith"
    expected_entities = {"John Smith"}
    entities = DataProcessor.extract_named_entities(text, mock_nlp)

    assert entities == expected_entities


def test_check_spelling_no_entities(mock_spellchecker):
    tokens = ["speeling", "mistke"]
    entities = set()
    corrected_tokens = DataProcessor.check_spelling(tokens, entities)
    assert corrected_tokens == tokens


def test_check_spelling_with_entities(mock_spellchecker):
    tokens = ["John", "Doe", "went", "to", "Prais"]
    entities = {"John Doe"}
    expected_tokens = [
        "John",
        "Doe",
        "went",
        "to",
        "Prais",
    ]
    corrected_tokens = DataProcessor.check_spelling(tokens, entities)
    assert corrected_tokens == expected_tokens


def test_remove_stop_words():
    tokens = ["this", "is", "not", "a", "test"]
    expected_result = ["not", "test"]
    actual_result = DataProcessor.remove_stop_words(tokens)
    assert actual_result == expected_result


def test_lemmatize_tokens(mock_nlp):
    mock_token1 = MagicMock()
    mock_token1.lemma_ = "run"

    mock_token2 = MagicMock()
    mock_token2.lemma_ = "eat"

    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = iter([mock_token1, mock_token2])

    mock_nlp.return_value = mock_doc

    tokens = ["running", "eats"]
    expected_lemmas = ["run", "eat"]
    lemmatized_tokens = DataProcessor.lemmatize_tokens(tokens, mock_nlp)

    assert lemmatized_tokens == expected_lemmas
