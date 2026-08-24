const screens = document.querySelectorAll('.screen');
const setupForm = document.querySelector('#setup-form');
const answerForm = document.querySelector('#answer-form');
const answerInput = document.querySelector('#answer');
const answerButton = document.querySelector('#answer-button');
const feedback = document.querySelector('#answer-feedback');
let waitingForNextQuestion = false;

function showScreen(screenId) {
    screens.forEach((screen) => screen.classList.toggle('active', screen.id === screenId));
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.querySelectorAll('[data-screen]').forEach((button) => {
    button.addEventListener('click', () => showScreen(button.dataset.screen));
});

document.querySelectorAll('.choice-card input').forEach((input) => {
    input.addEventListener('change', () => {
        document.querySelectorAll(`input[name="${input.name}"]`).forEach((option) => {
            option.closest('.choice-card').classList.toggle('selected', option.checked);
        });
    });
});

setupForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(setupForm);
    const error = document.querySelector('#setup-error');
    error.textContent = '';

    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                subject: formData.get('subject'),
                question_count: Number(formData.get('question_count')),
            }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error);
        renderQuestion(data);
        showScreen('quiz-screen');
        answerInput.focus();
    } catch (requestError) {
        error.textContent = requestError.message;
    }
});

answerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (waitingForNextQuestion) {
        return;
    }

    const answer = answerInput.value;
    if (!answer.trim()) return;
    answerButton.disabled = true;

    try {
        const response = await fetch('/api/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error);
        showFeedback(data.result);

        if (data.complete) {
            setTimeout(() => renderResults(data.results), 750);
        } else {
            waitingForNextQuestion = true;
            answerButton.disabled = false;
            answerButton.textContent = 'Next question  ->';
            answerButton.onclick = () => {
                waitingForNextQuestion = false;
                answerButton.onclick = null;
                answerButton.textContent = 'Submit answer  ->';
                feedback.textContent = '';
                answerInput.value = '';
                renderQuestion(data.question);
                answerInput.focus();
            };
        }
    } catch (requestError) {
        feedback.textContent = requestError.message;
        answerButton.disabled = false;
    }
});

function renderQuestion(question) {
    document.querySelector('#question-count').textContent = `Question ${question.number} / ${question.total}`;
    document.querySelector('#difficulty').textContent = question.difficulty;
    document.querySelector('#question-topic').textContent = question.topic;
    document.querySelector('#question-text').textContent = question.question;
    document.querySelector('#quiz-progress').style.width = `${(question.number / question.total) * 100}%`;
}

function showFeedback(result) {
    feedback.className = `feedback ${result.correct ? 'correct' : 'incorrect'}`;
    feedback.textContent = result.correct ? 'Correct. Nice work.' : `Not quite. The answer is ${result.correct_answer}.`;
}

function renderResults(results) {
    document.querySelector('#result-score').textContent = `${results.score} / ${results.total}`;
    document.querySelector('#result-percentage').textContent = `${results.percentage}%`;
    document.querySelector('#result-rating').textContent = results.rating;
    document.querySelector('#weakest-topic').textContent = results.weakest_topic;

    const topicResults = document.querySelector('#topic-results');
    topicResults.innerHTML = Object.entries(results.topics).map(([topic, result]) => {
        const percentage = (result.correct / result.total) * 100;
        return `<div class="topic-row"><div><strong>${topic}</strong><span>${result.correct} / ${result.total}</span></div><div class="topic-track"><div style="width: ${percentage}%"></div></div></div>`;
    }).join('');

    answerForm.reset();
    answerButton.disabled = false;
    answerButton.onclick = null;
    showScreen('results-screen');
}
