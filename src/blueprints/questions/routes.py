from flask import render_template, redirect, url_for

from src.blueprints.questions import bp
from src.blueprints.questions.forms import OpenQuestionForm, IntQuestionForm, BoolQuestionForm

# Route for the question page (both GET and POST)
@bp.route('/questionlist/question', methods=['GET', 'POST'])
def question():
    form = OpenQuestionForm()
    form.answer.label.text = "Testvraag?"
    if form.validate_on_submit():
        answer = form.answer.data
        return redirect(url_for('questions.question'))
    return render_template('form.html', form=form)