import requests
from ..utils.utilities import save_json_data


class GoogleBooksDataPopulator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def fetch_books(self, query):
        params = {
            "key": self.api_key,
            "q": query,
            "maxResults": 40,
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

    def populate_datastore(self, genre_queries):
        all_books = []
        all_authors = set()

        for query in genre_queries:
            response = self.fetch_books(query)
            books, authors = self.transform_book_data(response.get("items", []))
            all_books.extend(books)
            all_authors.update(authors)

        save_json_data(all_books, "data/books.json")
        save_json_data(list(all_authors), "data/authors.json")
