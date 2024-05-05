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


def test_identify_entities(mock_spacy_nlp):
    mock_ent_person = MagicMock(text="Stephen King", label_="PERSON")
    mock_ent_org = MagicMock(text="Science Fiction", label_="ORG")
    mock_ent_work_of_art = MagicMock(text="Bible", label_="WORK_OF_ART")
    mock_ent_date = MagicMock(text="21st September 1947", label_="DATE")
    mock_ent_language = MagicMock(text="English", label_="LANGUAGE")

    mock_spacy_nlp.return_value.ents = [
        mock_ent_person,
        mock_ent_org,
        mock_ent_work_of_art,
        mock_ent_date,
        mock_ent_language,
    ]

    recogniser = IntentRecogniser(
        genres=["fantasy", "sci-fi"], model_name="en_core_web_trf"
    )
    entities = recogniser.identify_entities(
        """Stephen King, born on the 21st September 1947, writes science fiction books and occasionally reads the Bible. 
        He speaks English as his main language"""
    )

    expected_entities = [
        ("Stephen King", "PERSON"),
        ("Science Fiction", "ORG"),
        ("Bible", "WORK_OF_ART"),
        ("21st September 1947", "DATE"),
        ("English", "LANGUAGE"),
    ]
    assert entities == expected_entities


def test_determine_query_intent(intent_recogniser):
    preprocessed_tokens = ["I", "want", "to", "read", "a", "fantasy", "book"]
    named_entities = []
    intents = intent_recogniser.get_query_intents(preprocessed_tokens, named_entities)
    assert "genre_recommendation" in intents

    preprocessed_tokens = []
    named_entities = [("Stephen King", "PERSON")]
    intents = intent_recogniser.get_query_intents(preprocessed_tokens, named_entities)
    assert "author_query" in intents

    preprocessed_tokens = ["This", "is", "an", "unrelated", "sentence"]
    named_entities = []
    intents = intent_recogniser.get_query_intents(preprocessed_tokens, named_entities)
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
