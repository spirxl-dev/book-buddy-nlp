import pytest
from unittest.mock import patch, MagicMock
from src.services.aggregators.google_books_aggregator import GoogleBooksAggregator


@pytest.fixture
def api_key():
    return "fake-api-key"


@pytest.fixture
def aggregator(api_key):
    return GoogleBooksAggregator(api_key)


@pytest.fixture
def sample_api_response():
    return {
        "items": [
            {
                "volumeInfo": {
                    "title": "Example Book",
                    "authors": ["Author One"],
                    "publishedDate": "2021",
                    "publisher": "Example Publisher",
                    "pageCount": 123,
                    "industryIdentifiers": [
                        {"type": "ISBN_13", "identifier": "9781234567890"}
                    ],
                    "categories": ["Fiction"],
                    "maturityRating": "MATURE",
                },
                "accessInfo": {"publicDomain": False},
            }
        ]
    }


def test_init(aggregator):
    assert aggregator.api_key == "fake-api-key"
    assert aggregator.base_url == "https://www.googleapis.com/books/v1/volumes"


@patch("requests.get")
def test_fetch_books(mock_get, aggregator, sample_api_response):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: sample_api_response)
    query = "fiction"
    response = aggregator.fetch_books(query)
    mock_get.assert_called_once_with(
        "https://www.googleapis.com/books/v1/volumes",
        params={"key": aggregator.api_key, "q": query, "maxResults": 10},
    )
    assert response == sample_api_response


def test_transform_book_data(aggregator, sample_api_response):
    transformed = aggregator.transform_book_data(sample_api_response["items"])
    expected = [
        {
            "title": "example book",
            "authors": ["author one"],
            "publishedDate": "2021",
            "publisher": "example publisher",
            "pageCount": 123,
            "isbn": "9781234567890",
            "genres": ["fiction"],
            "maturityRating": "mature",
            "isPublicDomain": False,
        }
    ]
    assert transformed == expected


@patch("src.services.aggregators.google_books_aggregator.GoogleBooksAggregator.fetch_books")
@patch(
    "src.services.aggregators.google_books_aggregator.GoogleBooksAggregator.transform_book_data"
)
def test_download_books(mock_transform, mock_fetch, aggregator, sample_api_response):
    mock_fetch.return_value = sample_api_response
    mock_transform.return_value = sample_api_response["items"]
    books = aggregator.download_books()
    assert len(books) == len(aggregator.genres)
    assert mock_fetch.call_count == len(aggregator.genres)
    assert mock_transform.call_count == len(aggregator.genres)


@patch("src.services.aggregators.google_books_aggregator.GoogleBooksAggregator.download_books")
@patch("builtins.open", new_callable=MagicMock)
@patch("src.services.aggregators.google_books_aggregator.save_json_data")
def test_download_and_save_books_non_empty(
    mock_save_json_data, mock_open, mock_download_books, aggregator
):

    mock_books = [{"title": "Effective Python", "isbn": "1234567890123"}]
    mock_download_books.return_value = mock_books

    output_path = "fake/path/to/output.json"
    aggregator.download_and_save_books(output_path)

    mock_save_json_data.assert_called_once_with(mock_books, output_path)


@patch("src.services.aggregators.google_books_aggregator.GoogleBooksAggregator.download_books")
@patch("builtins.open", new_callable=MagicMock)
@patch("src.services.aggregators.google_books_aggregator.save_json_data")
def test_download_and_save_books_empty(
    mock_save_json_data, mock_download_books, aggregator
):
    mock_download_books.return_value = []

    output_path = "fake/path/to/output.json"
    aggregator.download_and_save_books(output_path)
    mock_save_json_data.assert_not_called()
