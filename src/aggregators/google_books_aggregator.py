import requests
from ..utils.utilities import (
    load_json_data,
    save_json_data,
)


class GoogleBooksAggregator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def fetch_books(self, query):
        params = {
            "key": self.api_key,
            "q": query,
            "maxResults": 30,
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def transform_book_data(self, items):
        books = []
        authors = set()
        for item in items:
            volume_info = item.get("volumeInfo", {})
            book = {
                "title": volume_info.get("title"),
                "authors": volume_info.get("authors", []),
                "publishedDate": volume_info.get("publishedDate"),
                "isbn": next(
                    (
                        identifier["identifier"]
                        for identifier in volume_info.get("industryIdentifiers", [])
                        if identifier["type"] == "ISBN_13"
                    ),
                    None,
                ),
            }
            books.append(book)
            authors.update(book["authors"])
        return books, authors

    def download_books_by_genre(self, genres_json_path) -> list:
        genres = load_json_data(genres_json_path)
        genre_queries = []
        for genre in genres:
            genre_queries.append("subject:" + genre)

        all_books = []
        for query in genre_queries:
            response = self.fetch_books(query)
            books, _ = self.transform_book_data(response.get("items", []))
            all_books.extend(books)
        return all_books

    def download_authors_by_genre(self, genres_json_path) -> set:
        genres = load_json_data(genres_json_path)
        genre_queries = []
        for genre in genres:
            genre_queries.append("subject:" + genre)

        all_authors = set()
        for query in genre_queries:
            response = self.fetch_books(query)
            _, authors = self.transform_book_data(response.get("items", []))
            all_authors.update(authors)
        return all_authors

    def download_and_save_books(self, genres_path, output_path):
        books = self.download_books_by_genre(genres_path)
        save_json_data(books, output_path)

    def download_and_save_authors(self, genres_path, output_path):
        authors = self.download_authors_by_genre(genres_path)
        save_json_data(list(authors), output_path)
