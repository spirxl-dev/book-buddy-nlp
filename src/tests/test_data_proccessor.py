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
        assert DataProcessor.expand_contractions(contraction) == expected, f"Failed on contraction: {contraction}"



# def test_strip_punctuation():
#     test_text = "Hello, world! This is great."
#     expected_text = "Hello world This is great"
#     assert DataProcessor.strip_punctuation(test_text) == expected_text


# def test_normalise_case():
#     test_text = "This Should Be Lowercase."
#     expected_text = "this should be lowercase."
#     assert DataProcessor.normalise_case(test_text) == expected_text


# # Test for tokenize_text
# def test_tokenize_text():
#     test_text = "This is a test."
#     expected_tokens = [
#         "This",
#         "is",
#         "a",
#         "test",
#         ".",
#     ]  # Adjust based on the tokenizer's specifics
#     assert DataProcessor.tokenize_text(test_text) == expected_tokens


# def test_remove_stop_words():
#     test_tokens = ["this", "is", "a", "test", "not", "a", "drill"]
#     # Assuming "is", "a" are stop words, but we're keeping "not" as per the preserve_words set
#     expected_result = ["this", "test", "not", "drill"]
#     assert DataProcessor.remove_stop_words(test_tokens) == expected_result
