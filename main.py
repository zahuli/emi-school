from flask import Flask, render_template, request
import random

app = Flask(__name__)


def generate_addition_problem():
    a = random.randint(0, 9)
    b = random.randint(0, 9 - a)  # Ensuring sum is within limits
    return a, b, a + b


def generate_subtraction_problem():
    a = random.randint(1, 9)
    b = random.randint(0, a)  # Ensuring no negative results
    return a, b, a - b


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
