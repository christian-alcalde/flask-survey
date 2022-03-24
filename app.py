from nis import cat
from warnings import catch_warnings
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def index():
    """Generate survey form"""

    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=survey_title,
        instructions=survey_instructions)

@app.post("/begin")
def begin_survey():
    """Redirects to first question"""

    session['responses']= []

    return redirect("/questions/0")


def find_correct_question():
    """Find correct question index"""
    responses = session['responses']
    correct_question = len(responses)
    return correct_question

@app.get("/questions/<int:question_id>")
def show_question(question_id):
    """Displays question and redirects as needed"""
    correct_question = find_correct_question()

    if correct_question == len(survey.questions):
        return redirect("/complete")

    if question_id > len(survey.questions) or question_id is not correct_question:
        if correct_question == len(survey.questions):
            return redirect("/complete")
        flash("Please answer the questions in order!")
        return redirect(f"/questions/{correct_question}")

    question_string = survey.questions[question_id].question
    question_choices = survey.questions[question_id].choices

    return render_template(
        "question.html",
        choices = question_choices,
        question = question_string)


@app.post("/answer")
def submit_answer():
    """Appends answer to the response session"""

    responses = session['responses']
    responses.append(request.form["answer"])
    session['responses']=responses

    correct_question = find_correct_question()
    if correct_question == len(survey.questions):
        return redirect("/complete")

    return redirect(f"/questions/{correct_question}")

@app.get("/complete")
def complete_survey():
    """Redirects user to completion page"""
    print(session['responses'])
    return render_template("completion.html")