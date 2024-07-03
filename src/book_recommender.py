from src.utils.utilities import load_json_data


class BookRecommender:
    def __init__(self, json_file_path):
        self.books = load_json_data(json_file_path)

    def recommend(self, preferences):
        recommended_books: list = []
        genre_preferences = preferences.get("genres", set())
        author_preferences = preferences.get("authors", set())
        works_of_art_preferences = preferences.get("works_of_art", set())
        dates_preferences = preferences.get("dates", set())
        language_preferences = preferences.get("language", set())

        for book in self.books:
            book_genres = set(book.get("genres", []))
            book_authors = set(book.get("authors", []))
            book_titles = {book.get("title", "").lower()}
            book_dates = {str(book.get("publishedDate", ""))}
            book_languages = {book.get("language", "").lower()}

            genre_match = not genre_preferences or book_genres.intersection(
                genre_preferences
            )
            author_match = not author_preferences or book_authors.intersection(
                author_preferences
            )
            works_of_art_match = (
                not works_of_art_preferences
                or book_titles.intersection(works_of_art_preferences)
            )
            date_match = not dates_preferences or book_dates.intersection(
                dates_preferences
            )
            language_match = not language_preferences or book_languages.intersection(
                language_preferences
            )

            if (
                genre_match
                and author_match
                and works_of_art_match
                and date_match
                and language_match
            ):
                recommended_books.append(book)

        return recommended_books
