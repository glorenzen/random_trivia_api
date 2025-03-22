from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import app.db

tags_metadata = [
    {
        "name": "questions",
        "description": "Operations for Questions like getting, creating etc.",
    },
    {"name": "categories", "description": "Operations for question Categories."},
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

from app.routers import category, question, user
import uvicorn

app.include_router(category.router)
app.include_router(question.router)
app.include_router(user.router)


@app.get("/")
def index():
    return {"message": "Welcome to the Random Trivia API!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
