from fastapi import APIRouter

router = APIRouter()

# Dummy data
user_preferences = {
    "favorite_genres": ["Mystery", "Fantasy"],
    "favorite_authors": ["Agatha Christie", "J.K. Rowling"],
    "reading_level": "Intermediate",
    "preferred_book_length": "Medium",
    "reading_goals": ["Explore new genres", "Read classics"],
    "language_preference": "English",
}


@router.get("/preferences")
def get_preferences():
    return user_preferences

@router.put("/preferences")
def update_preferences(updated_preferences: dict):
    # Logic to update user preferences
    user_preferences.update(updated_preferences)
    return user_preferences