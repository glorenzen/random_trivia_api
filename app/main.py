from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import app.db

app = FastAPI()

from app.routers import category, question

app.include_router(category.router)
app.include_router(question.router)


@app.get("/")
def index():
    return {"message": "Welcome to the Random Trivia API!"}
