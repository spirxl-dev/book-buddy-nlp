from src.utils.utilities import load_json_data


class RecommendationEngine:
    def __init__(self, json_file_path):
        self.books = load_json_data(json_file_path)

    def recommend(self, preferences):
        recommended_books = []
        genre_preferences = preferences.get("genres", set())
        author_preferences = preferences.get("authors", set())

        for book in self.books:
            book_genres = set(book.get("genres", []))
            book_authors = set(book.get("authors", []))

            if (
                not genre_preferences or book_genres.intersection(genre_preferences)
            ) and (
                not author_preferences or book_authors.intersection(author_preferences)
            ):
                recommended_books.append(book)

        return recommended_books
