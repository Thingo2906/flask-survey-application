
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
responses =[]

@app.route("/")
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instruction = instructions)

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""
    # get the response choice
    choice = request.form['answer']
    # add this response to the list of responses
    responses.append(choice)
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions!
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:id>")
def show_question(id):
    """Display current question."""
    
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len( satisfaction_survey.questions)):
        # They've answered all the questions!
        return redirect("/complete")

    if (len(responses) != id):
        # Trying to access questions out of order.
        flash("Invalid question id")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[id]
    return render_template("question.html", question_num = id, question = question)



@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")
