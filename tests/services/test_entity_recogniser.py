import pytest
from unittest.mock import MagicMock
from src.services.entity_recogniser import EntityRecogniser


@pytest.fixture
def mock_spacy_nlp(mocker):
    mock_nlp = mocker.MagicMock()
    mocker.patch("spacy.load", return_value=mock_nlp)
    return mock_nlp


@pytest.fixture
def intent_recogniser():
    genres = ["fantasy", "sci-fi", "romance"]
    return EntityRecogniser(genres, "en_core_web_trf")


def test_entities(mock_spacy_nlp):
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

    recogniser = EntityRecogniser(
        genres=["fantasy", "sci-fi"], model_name="en_core_web_trf"
    )
    entities = recogniser.return_entities(
        "Stephen King wrote The Dark Tower. He was born on 21st September 1947 and speaks English."
    )

    expected_entities = [
        {"entity": "Stephen King", "type": "PERSON"},
        {"entity": "Science Fiction", "type": "ORG"},
        {"entity": "The Dark Tower", "type": "WORK_OF_ART"},
        {"entity": "21st September 1947", "type": "DATE"},
        {"entity": "English", "type": "LANGUAGE"},
    ]
    assert entities == expected_entities
