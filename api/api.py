import uvicorn
from fastapi import FastAPI
from routers import recommendations, search, preferences

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


# Search via a user query. e.g "Give me a sci fi book by stephen king"
app.include_router(search.router)


# TODO: Logic to fetch personalised book recommendations based on predefined preferences
# app.include_router(preferences.router)
# app.include_router(recommendations.router)


if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)