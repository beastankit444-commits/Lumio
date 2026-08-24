# Lumio v1.0

**Study smarter. Adapt faster.**

Lumio is a Flask website built around a simple adaptive quiz engine for Math, Physics, and Chemistry. It chooses questions at the current difficulty, moves up after a correct answer, and moves down after an incorrect answer.

This project is rule-based. It is not a machine-learning model or an AI tutor.

## Features

- Mixed, Math, Physics, and Chemistry sessions
- 5, 10, 15, or 20 questions
- Difficulty levels from 1 to 3
- Random questions without repeats in one session
- Difficulty adapts after every answer
- Correct-answer feedback after submission
- Score, percentage, correct/wrong totals, and rating
- Topic performance and weakest-topic detection
- Responsive single-page-style interface

## Tech Stack

- Python 3
- Flask
- HTML
- CSS
- Vanilla JavaScript

## Project Structure

```text
Lumio/
├── app.py                  Flask routes and browser API
├── quiz.py                 Adaptive quiz and results logic
├── questions.py            Copied question bank
├── studyAI_original.py     Original script snapshot for reference
├── requirements.txt        Python dependency list
├── templates/index.html    Website screens
├── static/style.css        Visual design and responsive layout
├── static/script.js        Browser interactions and API calls
├── README.md               Project documentation
└── .gitignore              Git exclusions
```

## Installation

From the `Lumio` folder, create and activate a virtual environment:

```text
python -m venv .venv
.venv\Scripts\activate
```

Install Flask:

```text
pip install -r requirements.txt
```

## Run

```text
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Publish For Free With Render

Think of it this way: GitHub is the cupboard where your code lives. Render is the computer that keeps your website open for visitors.

1. Create a free account at [render.com](https://render.com).
2. Create a new GitHub repository and upload the contents of this `Lumio` project.
3. In Render, choose **New +** and then **Web Service**.
4. Choose your GitHub repository.
5. If the repository contains this project inside another folder, set **Root Directory** to `orogeny codes/AIStudy`. If this project is the whole repository, leave it blank.
6. Set **Build Command** to:

```text
pip install -r requirements.txt
```

7. Set **Start Command** to:

```text
gunicorn app:app
```

8. Choose the free plan and click **Create Web Service**.
9. Wait for Render to finish. It will give you a public web address.
10. Share that address. Anyone with the link can open Lumio.

The free service may go to sleep when nobody is using it. The first visit after sleeping can take a little longer. The website also needs internet access because Flask is the part serving the pages.

## How Adaptation Works

Each question keeps the original structure:

```python
{
    "question": "What is 15*8?",
    "answer": "120",
    "topic": "math",
    "difficulty": 1
}
```

A quiz starts at difficulty 1. A correct answer increases the next difficulty by one, up to 3. An incorrect answer decreases it by one, down to 1. Previously asked question objects are stored in the current session and excluded from later choices.

The browser sends answers to Flask. Flask passes them to `QuizSession`, which checks the answer and updates the score. Flask then sends back feedback and the next question. The answer key stays on the server.

## Future Plans

- Add more carefully reviewed questions
- Add optional quiz history without changing the simple core
- Add automated tests for the quiz engine

## Release

See `RELEASE_NOTES.md` for the v1.0 release summary.
