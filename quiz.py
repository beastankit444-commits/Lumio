import random

from questions import questions


class QuizSession:
    """Keep the state for one adaptive quiz."""

    def __init__(self, subject, question_count):
        self.subject = subject
        self.question_count = question_count
        self.difficulty = 1
        self.score = 0
        self.current_question = None
        self.asked_questions = []
        self.topic_score = {"math": 0, "physics": 0, "chemistry": 0}
        self.correct_by_topic = {"math": 0, "physics": 0, "chemistry": 0}

    def _available_questions(self):
        return [
            question for question in questions
            if (self.subject == "mixed" or question["topic"] == self.subject)
            and question not in self.asked_questions
        ]

    def next_question(self):
        available_questions = [
            question for question in self._available_questions()
            if question["difficulty"] == self.difficulty
        ]

        # If a subject has no unused questions at this level, keep the quiz moving.
        if not available_questions:
            available_questions = self._available_questions()

        self.current_question = random.choice(available_questions)
        self.asked_questions.append(self.current_question)
        self.topic_score[self.current_question["topic"]] += 1

        return {
            "question": self.current_question["question"],
            "topic": self.current_question["topic"],
            "difficulty": self.current_question["difficulty"],
            "number": len(self.asked_questions),
            "total": self.question_count,
        }

    def submit_answer(self, answer):
        if self.current_question is None:
            raise ValueError("There is no question waiting for an answer.")

        correct_answer = self.current_question["answer"]
        is_correct = answer.strip().lower() == correct_answer.strip().lower()
        topic = self.current_question["topic"]

        if is_correct:
            self.score += 1
            self.correct_by_topic[topic] += 1
            self.difficulty = min(3, self.difficulty + 1)
        else:
            self.difficulty = max(1, self.difficulty - 1)

        return {
            "correct": is_correct,
            "correct_answer": correct_answer,
            "next_difficulty": self.difficulty,
        }

    def results(self):
        percentage = (self.score / self.question_count) * 100
        attempted_topics = [
            topic for topic in self.topic_score
            if self.topic_score[topic] > 0
        ]
        weakest_topic = min(
            attempted_topics,
            key=lambda topic: self.correct_by_topic[topic] / self.topic_score[topic]
        )

        if percentage >= 90:
            rating = "Excellent"
        elif percentage >= 75:
            rating = "Very Good"
        elif percentage >= 50:
            rating = "Needs Improvement"
        else:
            rating = "Keep Practicing"

        topic_results = {
            topic: {
                "correct": self.correct_by_topic[topic],
                "total": self.topic_score[topic],
            }
            for topic in attempted_topics
        }

        return {
            "score": self.score,
            "total": self.question_count,
            "percentage": round(percentage, 1),
            "wrong": self.question_count - self.score,
            "rating": rating,
            "weakest_topic": weakest_topic,
            "topics": topic_results,
        }
