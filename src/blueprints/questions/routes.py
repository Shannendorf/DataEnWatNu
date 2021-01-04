from flask import render_template, redirect, url_for, request

from src.blueprints.questions import bp
from src.blueprints.questions.forms import OpenQuestionForm, IntQuestionForm, BoolQuestionForm, get_form
from src.models import Question, QuestionType, Answer

# Route for the question page (both GET and POST)
@bp.route('/questionlist/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    #session_id = 12 #request.cookies.get('sessionID')
    question_order = [1,3,2]
    question = Question.get_by_id(question_order[question_id])    
    formtype = QuestionType.query().filter_by(name=Question.questiontype).first().name
    form = get_form(formtype)
    form.answer.label.text = question.question
    
    if form.validate_on_submit():
        answer = form.answer.data
        #Answer.create(answer=answer, answeredquestion=question.id, case=2)
        return redirect(url_for('questions.question', question_id=question_id+1))
    return render_template('form.html', form=form)