import pytest
from unittest.mock import MagicMock
from src.intent_recogniser import IntentRecogniser


@pytest.fixture
def mock_spacy_nlp(mocker):
    mock_nlp = mocker.MagicMock()
    mocker.patch("spacy.load", return_value=mock_nlp)
    return mock_nlp


@pytest.fixture
def intent_recogniser():
    genres = ["fantasy", "sci-fi", "romance"]
    return IntentRecogniser(genres, "en_core_web_trf")


def test_extract_entities(mock_spacy_nlp):
    mock_ent1 = MagicMock(text="Stephen King", label_="PERSON")
    mock_ent2 = MagicMock(text="Science Fiction", label_="ORG")
    mock_spacy_nlp.return_value.ents = [mock_ent1, mock_ent2]

    recogniser = IntentRecogniser(
        genres=["fantasy", "sci-fi"], model_name="en_core_web_trf"
    )
    entities = recogniser.extract_entities("Stephen King writes Science Fiction books.")

    expected_entities = [("Stephen King", "PERSON"), ("Science Fiction", "ORG")]
    assert entities == expected_entities


def test_determine_query_intent(intent_recogniser):
    preprocessed_tokens = ["I", "want", "to", "read", "a", "fantasy", "book"]
    named_entities = []
    intents = intent_recogniser.determine_query_intent(
        preprocessed_tokens, named_entities
    )
    assert "genre_recommendation" in intents

    preprocessed_tokens = []
    named_entities = [("Stephen King", "PERSON")]
    intents = intent_recogniser.determine_query_intent(
        preprocessed_tokens, named_entities
    )
    assert "author_query" in intents

    preprocessed_tokens = ["This", "is", "an", "unrelated", "sentence"]
    named_entities = []
    intents = intent_recogniser.determine_query_intent(
        preprocessed_tokens, named_entities
    )
    assert "unknown" in intents


def test_extract_intent_details_for_genres(intent_recogniser):
    preprocessed_tokens = ["I", "love", "fantasy", "and", "sci-fi"]
    named_entities = []  # Not relevant for this test
    details = intent_recogniser.extract_intent_details(
        preprocessed_tokens, named_entities, "genres"
    )
    assert details == {"fantasy", "sci-fi"}


def test_extract_intent_details_for_authors(intent_recogniser):
    preprocessed_tokens = []  # Not relevant for this test
    named_entities = [("George Orwell", "PERSON"), ("Big Brother", "ORG")]
    details = intent_recogniser.extract_intent_details(
        preprocessed_tokens, named_entities, "author"
    )
    assert details == {"George Orwell"}
