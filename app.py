import os

from flask import Flask, jsonify, render_template, request, session

from quiz import QuizSession

app = Flask(__name__)
app.config["SECRET_KEY"] = "lumio-v1-development-key"


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/start")
def start_quiz():
    data = request.get_json(silent=True) or {}
    subject = data.get("subject", "mixed")
    question_count = data.get("question_count", 10)

    if subject not in {"mixed", "math", "physics", "chemistry"}:
        return jsonify({"error": "Choose a valid subject."}), 400
    if question_count not in {5, 10, 15, 20}:
        return jsonify({"error": "Choose a valid question count."}), 400

    quiz = QuizSession(subject, question_count)
    session["quiz"] = quiz.__dict__
    return jsonify(_question_response(quiz))


@app.post("/api/answer")
def answer_question():
    quiz = _load_quiz()
    if quiz is None:
        return jsonify({"error": "Start a quiz first."}), 400

    data = request.get_json(silent=True) or {}
    result = quiz.submit_answer(data.get("answer", ""))
    is_complete = len(quiz.asked_questions) >= quiz.question_count
    response = {"result": result, "complete": is_complete}

    if is_complete:
        response["results"] = quiz.results()
    else:
        response["question"] = _question_response(quiz)

    _save_quiz(quiz)
    return jsonify(response)


def _question_response(quiz):
    return quiz.next_question()


def _load_quiz():
    saved_quiz = session.get("quiz")
    if saved_quiz is None:
        return None

    quiz = QuizSession(saved_quiz["subject"], saved_quiz["question_count"])
    quiz.__dict__.update(saved_quiz)
    return quiz


def _save_quiz(quiz):
    session["quiz"] = quiz.__dict__


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )
