from flask import Flask, render_template, request
import random

app = Flask(__name__)

used_addition_problems = set()
used_subtraction_problems = set()


used_addition_problems = set()


def generate_addition_problem():
    attempts = 0
    while True:
        a = random.randint(1, 8)  # max 8 so b can be at least 1
        max_b = 9 - a
        if max_b < 1:
            continue  # skip to avoid invalid range
        b = random.randint(1, max_b)
        problem = (a, b)
        if problem not in used_addition_problems:
            used_addition_problems.add(problem)
            return a, b, a + b
        attempts += 1
        if attempts > 30:
            used_addition_problems.clear()


def generate_subtraction_problem():
    attempts = 0
    while True:
        a = random.randint(1, 9)
        b = random.randint(1, a)
        problem = (a, b)
        if problem not in used_subtraction_problems:
            used_subtraction_problems.add(problem)
            return a, b, a - b
        attempts += 1
        if attempts > 30:
            used_subtraction_problems.clear()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addition', methods=['GET', 'POST'])
def addition():
    if request.method == 'GET':
        a, b, correct_answer = generate_addition_problem()
        message = ""
    else:
        try:
            a = int(request.form['a'])
            b = int(request.form['b'])
            correct_answer = int(request.form['correct_answer'])
            user_answer = request.form.get('answer')

            if user_answer and user_answer.strip():
                if int(user_answer) == correct_answer:
                    message = "ТАЧАН ОДГОВОР! 😊"
                else:
                    message = "НЕТАЧАН ОДГОВОР! ❌"
            else:
                message = "МОЛИМ ВАС УНЕСИТЕ БРОЈ."
        except ValueError:
            message = "ПОГРЕШАН УНОС. УНЕСИТЕ БРОЈ."

    return render_template('math.html', a=a, b=b, correct_answer=correct_answer, operator='+', message=message)


@app.route('/subtraction', methods=['GET', 'POST'])
def subtraction():
    if request.method == 'GET':
        a, b, correct_answer = generate_subtraction_problem()
        message = ""
    else:
        try:
            a = int(request.form['a'])
            b = int(request.form['b'])
            correct_answer = int(request.form['correct_answer'])
            user_answer = request.form.get('answer')

            if user_answer and user_answer.strip():
                if int(user_answer) == correct_answer:
                    message = "ТАЧАН ОДГОВОР! 😊"
                else:
                    message = "НЕТАЧАН ОДГОВОР! ❌"
            else:
                message = "МОЛИМ ВАС УНЕСИТЕ БРОЈ."
        except ValueError:
            message = "ПОГРЕШАН УНОС. УНЕСИТЕ БРОЈ."

    return render_template('math.html', a=a, b=b, correct_answer=correct_answer, operator='-', message=message)


if __name__ == '__main__':
    app.run(debug=True)
