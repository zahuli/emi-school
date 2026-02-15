from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecret123"


used_addition_problems = set()
used_subtraction_problems = set()


def generate_addition_problem():
    if len(used_addition_problems) > 100:  # Updated limit for combinations up to 20
        used_addition_problems.clear()

    while True:
        a = random.randint(1, 18)  # Updated range for numbers up to 20
        max_b = 19 - a
        if max_b < 1:
            continue
        b = random.randint(1, max_b)
        problem = (a, b)
        if problem not in used_addition_problems:
            used_addition_problems.add(problem)
            return a, b, a + b


def generate_subtraction_problem():
    if len(used_subtraction_problems) > 100:  # Updated limit for combinations up to 20
        used_subtraction_problems.clear()

    while True:
        a = random.randint(1, 19)  # Updated range for numbers up to 20
        b = random.randint(1, a)
        problem = (a, b)
        if problem not in used_subtraction_problems:
            used_subtraction_problems.add(problem)
            return a, b, a - b


@app.route('/')
def home():
    session.clear()  # reset score and counter
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

@app.route('/addition_with_grade', methods=['GET', 'POST'])
def addition_with_grade():
    if "count" not in session:
        session["count"] = 0
        session["correct"] = 0
    
    if session["count"] >= 20:
        return redirect(url_for("grade_page", mode="addition"))

    # the first task or the next task
    if request.method == 'GET':
        a, b, correct = generate_addition_problem()
        session["a"] = a
        session["b"] = b
        session["correct_answer"] = correct
        message = ""
    else:
        try:
            session["a"] = int(request.form['a'])
            session["b"] = int(request.form['b'])
            session["correct_answer"] = int(request.form['correct_answer']) 
            user_answer = request.form.get("answer")

            if user_answer and user_answer.strip():
                if int(user_answer) == session["correct_answer"]:
                    message = "ТАЧАН ОДГОВОР! 😊"
                    session["correct"] += 1
                else:
                    message = "НЕТАЧАН ОДГОВОР! ❌"
            else:
                message = "МОЛИМ ВАС УНЕСИТЕ БРОЈ."
        except ValueError:
            message = "ПОГРЕШАН УНОС. УНЕСИТЕ БРОЈ."
        
        session["count"] += 1
        print(session)

    return render_template(
        "math_with_grade.html",
        a=session["a"],
        b=session["b"],
        operator="+",
        correct_answer=session["correct_answer"],
        correct_counter = session["correct"],
        message=message,
        counter=session["count"] + 1
    )

@app.route('/subtraction_with_grade', methods=['GET', 'POST'])
def subtraction_with_grade():
    if "count" not in session:
        session["count"] = 0
        session["correct"] = 0

    if session["count"] >= 20:
        return redirect(url_for("grade_page", mode="subtraction"))

    if request.method == 'GET':
        a, b, correct = generate_subtraction_problem()
        session["a"] = a
        session["b"] = b
        session["correct_answer"] = correct
        message = ""
    else:
        try:
            session["a"] = int(request.form['a'])
            session["b"] = int(request.form['b'])
            session["correct_answer"] = int(request.form['correct_answer']) 
            user_answer = request.form.get("answer")

            if user_answer and user_answer.strip():
                if int(user_answer) == session["correct_answer"]:
                    message = "ТАЧАН ОДГОВОР! 😊"
                    session["correct"] += 1
                else:
                    message = "НЕТАЧАН ОДГОВОР! ❌"
            else:
                message = "МОЛИМ ВАС УНЕСИТЕ БРОЈ."
        except ValueError:
            message = "ПОГРЕШАН УНОС. УНЕСИТЕ БРОЈ."

        session["count"] += 1
        print(session)

    return render_template(
        "math_with_grade.html",
        a=session["a"],
        b=session["b"],
        operator="-",
        correct_answer=session["correct_answer"],
        correct_counter = session["correct"],
        message=message,
        counter=session["count"] + 1
    )

@app.route('/grade/<mode>')
def grade_page(mode):
    correct = session.get("correct", 0)
    total = 20

    percent = correct / total

    if percent >= 0.9:
        grade = 5
    elif percent >= 0.75:
        grade = 4
    elif percent >= 0.6:
        grade = 3
    elif percent >= 0.4:
        grade = 2
    else:
        grade = 1

    return render_template(
        "grade.html",
        correct=correct,
        total=total,
        grade=grade,
        mode=mode
    )


if __name__ == '__main__':
    # app.run(debug=True)
    import os
    # default is arbitrary, Render always sets PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
