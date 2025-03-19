from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import app.db

app = FastAPI()

from app.routers import category, question
import uvicorn

app.include_router(category.router)
app.include_router(question.router)


@app.get("/")
def index():
    return {"message": "Welcome to the Random Trivia API!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
