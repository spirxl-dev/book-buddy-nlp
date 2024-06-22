import uvicorn
from fastapi import FastAPI
from api.routers import search

app = FastAPI()


app.include_router(search.router)


if __name__ == "__main__":
    uvicorn.run("api_run:app", host="localhost", port=8000, reload=True)
