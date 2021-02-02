from flask import render_template, redirect, url_for, request, make_response, send_file, current_app

from src.blueprints.questions import bp
from src.blueprints.questions.forms import OpenQuestionForm, IntQuestionForm, BoolQuestionForm, MCQuestionForm, EmailForm, get_form
from src.blueprints.questions.report_generator import generate_report
from src.blueprints.questions.email import send_email
from src.models import Question, QuestionType, Answer, Case


# Route for question startpage
@bp.route('/questions/start', methods=['GET', 'POST'])
def start():
    case = Case.create_case()
    session_id = case.id
    url = url_for("questions.question", question_id=0)
    html = f"<meta http-equiv='refresh' content='1; URL={url}'/>"

    # Sets the cookie
    resp = make_response(html)
    resp.set_cookie('sessionID', session_id, max_age=10800)
    return resp


# Route for the question page (both GET and POST)
@bp.route('/questionlist/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    session_id = request.cookies.get('sessionID')
    if not session_id:
        return redirect(url_for('questions.start'))        

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
    
    if formtype == "likert":
        form.nr = len(question.options)
        form.answer2.choices = answeroptions
        form.answer3.choices = answeroptions
        form.answer4.choices = answeroptions
        form.answer5.choices = answeroptions

    # Saves answer to db
    if form.validate_on_submit():
        answer = form.answer.data
        if Answer.query().filter_by(case=session_id, answeredquestion=question.id).count() != 0:
            to_change = Answer.query().filter_by(case=session_id, answeredquestion=question.id).first()
            to_change.update(answer=answer)
        else:
            Answer.create(answer=answer, answeredquestion=question.id, case=session_id)
        return redirect(url_for('questions.question', question_id=question_id+1))
    """if formtype == "likert":
        return render_template('likert.html', form=form, questions=["vraag 1?"])
    else:""" 
    return render_template('form.html', form=form)


# Route for advice page
@bp.route('/advice', methods=['GET', 'POST'])
def advice():
    # Checks whether there is a session_id, otherwise the user gets redirected
    # to the startpage
    session_id = request.cookies.get('sessionID')
    if not session_id:
        redirect(url_for('main.index'))

    # Renders the endpage
    answers = Answer.query().filter_by(case=session_id).all()
    form = EmailForm()
    answers_list = []
    for answer in answers:
        answers_list.append((answer.answered_question.question, answer.answer),)
    generate_report(answers_list, session_id)
    if form.validate_on_submit():
        email_address = [form.answer.data]
        send_email('Data en wat nu rapport', current_app.config['ADMINS'][0], email_address, 'In de bijlage treft u het Data en wat nu rapport aan.', 'In de bijlage treft u het Data en wat nu rapport aan.', session_id)
    return render_template('advice.html', extra_text="Dit is de eindpagina", title="Eindpagina", form=EmailForm(), answers=answers)

# Route for report download
@bp.route('/report', methods=['GET'])
def report():
    session_id = request.cookies.get('sessionID')
    if not session_id:
        redirect(url_for('main.index'))
    return send_file(
    'output/pdf/'+session_id+'.pdf',
    mimetype='application/pdf',
    attachment_filename='DataEnWatNu.pdf',
    as_attachment=True
    )