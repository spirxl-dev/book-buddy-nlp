import pytest
from src.data_processer import DataProcessor


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
        assert (
            DataProcessor.expand_contractions(contraction) == expected
        ), f"Failed on contraction: {contraction}"


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