from src.services.utils.utilities import load_json_data


class BookRecommender:
    def __init__(self, json_file_path):
        self.books = load_json_data(json_file_path)

    def recommend(self, entities: list, intents: list) -> list:
        genre_preferences = {
            ent["entity"].lower() for ent in entities if ent["type"] == "GENRE"
        }
        author_preferences = {
            ent["entity"].lower()
            for ent in entities
            if ent["type"] in ["PERSON", "ORG"]
        }
        works_of_art_preferences = {
            ent["entity"].lower() for ent in entities if ent["type"] == "WORK_OF_ART"
        }
        dates_preferences = {ent["entity"] for ent in entities if ent["type"] == "DATE"}
        language_preferences = {
            ent["entity"].lower() for ent in entities if ent["type"] == "LANGUAGE"
        }

        recommended_books: list = []

        for book in self.books:
            book_genres = set(book.get("genres", []))
            book_authors = {author.lower() for author in book.get("authors", [])}
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
