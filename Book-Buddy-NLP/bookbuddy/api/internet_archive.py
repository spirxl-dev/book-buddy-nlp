# This module handles communication with Internet Archive APIs to fetch book data.
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/internet_archive/{query}")
async def fetch_books_from_internet_archive(query: str):
    base_url = "http://archive.org/advancedsearch.php"
    params = {"q": query, "output": "json"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
