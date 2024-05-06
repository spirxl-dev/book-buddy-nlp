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
    mock_ent_work_of_art = MagicMock(text="The Dark Tower", label_="WORK_OF_ART")
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
        "Stephen King wrote The Dark Tower. He was born on 21st September 1947 and speaks English."
    )

    expected_entities = [
        ("Stephen King", "PERSON"),
        ("Science Fiction", "ORG"),
        ("The Dark Tower", "WORK_OF_ART"),
        ("21st September 1947", "DATE"),
        ("English", "LANGUAGE"),
    ]
    assert entities == expected_entities


def test_determine_query_intent(intent_recogniser):
    preprocessed_tokens = ["I", "want", "to", "read", "The Dark Tower"]
    named_entities = [("The Dark Tower", "WORK_OF_ART")]
    intents = intent_recogniser.get_query_intents(preprocessed_tokens, named_entities)
    assert "work_of_art_query" in intents

    preprocessed_tokens = []
    named_entities = [("21st September 1947", "DATE")]
    intents = intent_recogniser.get_query_intents(preprocessed_tokens, named_entities)
    assert "date_query" in intents


def test_extract_intent_details_for_works_of_art(intent_recogniser):
    preprocessed_tokens = []
    named_entities = [("The Dark Tower", "WORK_OF_ART")]
    details = intent_recogniser.extract_intent_details(
        preprocessed_tokens, named_entities, "work_of_art"
    )
    assert details == {"The Dark Tower"}


def test_extract_intent_details_for_dates(intent_recogniser):
    preprocessed_tokens = []
    named_entities = [("21st September 1947", "DATE")]
    details = intent_recogniser.extract_intent_details(
        preprocessed_tokens, named_entities, "date"
    )
    assert details == {"21st September 1947"}
