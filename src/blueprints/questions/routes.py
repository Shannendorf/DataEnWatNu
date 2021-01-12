from flask import render_template, redirect, url_for, request, make_response

from src.blueprints.questions import bp
from src.blueprints.questions.forms import OpenQuestionForm, IntQuestionForm, BoolQuestionForm, MCQuestionForm, EmailForm, get_form
from src.models import Question, QuestionType, Answer, Case

# Route for the question page (both GET and POST)
@bp.route('/questionlist/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    session_id = request.cookies.get('sessionID')
    if not session_id:
        case = Case.create_case()
        session_id = case.id

    # Retrieves correct question or redirects to endpage
    question_order = [1,4,3,2]
    if len(question_order) > question_id:
        question = Question.get_by_id(question_order[question_id])
    else:
        return redirect(url_for('questions.advice'))

    # Determines which form is appropriate and includes necessary information               
    formtype = QuestionType.query().filter_by(name=question.questiontype).first().name
    form = get_form(formtype)
    form.answer.label.text = question.question
    if formtype == "multiplechoice" or formtype == "likert":
        answeroptions = []
        for answeroption in question.options:
            answeroptions.append(answeroption)
        form.answer.choices = answeroptions
    
    """
    if formtype == "likert":
        form.nr = len(question.options)
        form.answer2.choices = answeroptions
        form.answer3.choices = answeroptions
        form.answer4.choices = answeroptions
        form.answer5.choices = answeroptions
        """ 

    # Sets the cookie
    if request.method == "GET":
        resp = make_response(render_template('form.html', form=form))
        resp.set_cookie('sessionID', session_id)
        return resp

    # Saves answer to db
    if form.validate_on_submit():
        answer = form.answer.data
        if Answer.query().filter_by(case=session_id, answeredquestion=question.id).count() != 0:
            to_change = Answer.query().filter_by(case=session_id, answeredquestion=question.id).first()
            to_change.update(answer=answer)
        else:
            Answer.create(answer=answer, answeredquestion=question.id, case=session_id)
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

    # Renders the endpage and resets the session_id in the cookie
    answers = Answer.query().filter_by(case=session_id).all()
    questions_and_answers = {}
    for a in answers:
        q = Question.query().filter_by(id=a.answeredquestion).first()
        questions_and_answers[q] = a
    resp = make_response(render_template('advice.html', extra_text="Dit is de eindpagina", title="Eindpagina", form=EmailForm(), questions_and_answers=questions_and_answers))
    resp.set_cookie('sessionID', '', expires=0)
    return resp