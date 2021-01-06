from flask import render_template, redirect, url_for, request, make_response

from src.blueprints.questions import bp
from src.blueprints.questions.forms import OpenQuestionForm, IntQuestionForm, BoolQuestionForm, get_form
from src.models import Question, QuestionType, Answer, Case

# Route for the question page (both GET and POST)
@bp.route('/questionlist/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    session_id = request.cookies.get('sessionID')
    if not session_id:
        case = Case.create_case()
        session_id = case.id

    question_order = [1,3,2]
    if question_order[question_id]:
        question = Question.get_by_id(question_order[question_id])
    else:
        return redirect(url_for('questions.advice'))            
    formtype = QuestionType.query().filter_by(name=Question.questiontype).first().name
    form = get_form(formtype)
    form.answer.label.text = question.question
    
    if request.method == "GET":
        resp = make_response(render_template('form.html', form=form))
        resp.set_cookie('sessionID', session_id)
        return resp

    if form.validate_on_submit():
        answer = form.answer.data
        Answer.create(answer=answer, answeredquestion=question.id, case=session_id)

        if question_order[-1] == question_id:
            return redirect(url_for('questions.advice'))

        return redirect(url_for('questions.question', question_id=question_id+1))
    return render_template('form.html', form=form)


# Route for advice page
@bp.route('/advice', methods=['GET', 'POST'])
def advice():
    # Checks whether there is a session_id, otherwise the user gets redirected
    # to the startpage
    session_id = request.cookies.get('sessionID')
    if not session_id:
        redirect(url_for('main.index'))

    # Renders the recommendation page and resets the session_id in the cookie
    resp = make_response(render_template('advice.html'))
    resp.set_cookie('sessionID', '', expires=0)
    return resp