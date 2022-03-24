from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def index():
    """Generate survey form"""

    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template("survey_start.html", title=survey_title, instructions=survey_instructions)

@app.post("/begin")
def begin_survey():
    """Redirects to first question"""

    return redirect("/questions/0")

@app.get("/questions/<int:question_id>")
def show_question(question_id):
    """Displays question"""
    question_string = survey.questions[question_id].question
    question_choices = survey.questions[question_id].choices

    return render_template("question.html", choices = question_choices, question = question_string)

@app.post("/answer")
def submit_answer():
    """"Appends answer to the response list"""
    responses.append(request.form["answer"])
    # print(responses)
    question_number = len(responses)
    if question_number == len(survey.questions):
        return redirect("/complete")
    else:
        link = f"/questions/{question_number}"
        return redirect(link)

@app.get("/complete")
def complete_survey():
    """Redirects user to completion page"""
    print(responses)
    return render_template("completion.html")