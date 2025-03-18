# Random Trivia API

This is a simple FastAPI project designed to provide random trivia questions across various topics such as:

- Film
- Literature
- Geography
- Science
- And more!

## Purpose

This project is really just practice while I learn FastAPI. It's not intended for any production use.

## Features

- Retrieve random trivia questions by topic. (Not yet)
- Explore a variety of trivia categories.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn (for running the development server)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/random_trivia_api.git
cd random_trivia_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the development server:

```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the API documentation.

## License

This project is for personal use and is not licensed for distribution.

---
