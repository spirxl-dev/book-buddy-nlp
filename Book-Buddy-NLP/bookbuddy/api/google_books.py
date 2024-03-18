# This module handles communication with Google Books APIs to fetch book data.
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/google_books/{query}")
async def fetch_books_from_google(query: str):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
