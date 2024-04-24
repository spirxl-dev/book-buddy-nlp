import requests
from ..utils.utilities import save_json_data
from config import GENRES


class GoogleBooksAggregator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        self.genres = GENRES

    def fetch_books(self, query):
        params = {
            "key": self.api_key,
            "q": query,
            "maxResults": 10,
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def transform_book_data(self, items):
        books = []
        for item in items:
            volume_info = item.get("volumeInfo", {})
            isbn_13 = None
            for identifier in volume_info.get("industryIdentifiers", []):
                if identifier["type"] == "ISBN_13":
                    isbn_13 = identifier["identifier"]
                    break

            book = {
                "title": volume_info.get("title"),
                "authors": volume_info.get("authors", []),
                "publishedDate": volume_info.get("publishedDate"),
                "publisher": volume_info.get("publisher", "Not Available"),
                "pageCount": volume_info.get("pageCount", "Unknown"),
                "isbn": isbn_13,
                "genres": volume_info.get("categories", ["Unknown"]),
                "maturityRating": volume_info.get("maturityRating", "Not Rated"),
                "isPublicDomain": item.get("accessInfo", {}).get("publicDomain", False),
            }
            books.append(book)
        return books

    def download_books_by_genre(self) -> list:
        genre_queries = []
        for genre in self.genres:
            genre_queries.append("subject:" + genre)

        all_books = []
        for query in genre_queries:
            response = self.fetch_books(query)
            books = self.transform_book_data(response.get("items", []))
            all_books.extend(books)
        return all_books

    def download_and_save_books(self, output_path):
        books = self.download_books_by_genre()
        save_json_data(books, output_path)
