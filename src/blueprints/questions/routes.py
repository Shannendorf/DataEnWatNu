from flask import render_template, redirect, url_for, request, make_response, \
    send_file, current_app, flash
from sqlalchemy.sql.expression import select

from src.blueprints.questions import bp
from src.blueprints.questions.forms import EmailForm, IntroForm, QuestionnaireForm, \
    LoginForm
from src.blueprints.questions.report_generator import generate_report
from src.blueprints.questions.email import send_email
from src.models import Question, QuestionType, Answer, Case, QuestionGroup, \
    Code, QuestionList


# Route for question startpage
@bp.route('/questions/start', methods=['GET', 'POST'])
def start():
    form = LoginForm()
    if form.validate_on_submit():
        code = Code.get_code(form.code.data)
        if code and code.active:
            case = Case.create_case(code)
            session_id = case.id
            resp = make_response(redirect(url_for("questions.intro")))
            resp.set_cookie("sessionID", session_id, max_age=10800)
            return resp
        flash("Code onjuist")
        return redirect(url_for("questions.start"))
    return render_template("login.html", form=form)


# Route for selecting the question list
@bp.route("/questions/intro", methods=["GET", "POST"])
def intro():
    session_id = request.cookies.get("sessionID")
    if not session_id:
        return redirect(url_for("questions.start"))
    case = Case.query().filter_by(id=session_id).first()
    if not case:
        return redirect(url_for("questions.start"))
    
    form = IntroForm()
    form.selection.choices = [(l.id, l.name) for l in QuestionList\
        .query().all()]
    if form.validate_on_submit():
        selected_list = QuestionList.get_by_id(form.selection.data)
        case.update(list_selected=selected_list.id)
        return redirect(url_for("questions.question", question_id=0))
    return render_template("intro.html", form=form)
        

# Route for the question page (both GET and POST)
@bp.route('/questionlist/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    session_id = request.cookies.get('sessionID')
    if not session_id:
        return redirect(url_for('questions.start'))
    case = Case.query().filter_by(id=session_id).first()
    if not case:
        return redirect(url_for("questions.start"))

    # Retrieves correct question group or redirects to endpage
    question_group_order = QuestionList.get_by_id(1).groups.all()
    question_group_order = case.case_list.groups.all()
    if len(question_group_order) <= question_id:
        return redirect(url_for("questions.advice"))
    question_group = question_group_order[question_id]

    # Determines which form is appropriate and includes necessary information               
    form, question_fields = QuestionnaireForm(question_group,
        submit_text="Bevestig")

    # Saves answers to db
    if form.validate_on_submit():
        for question_label, question_obj in question_fields.items():
            answer_data = getattr(form, question_label).data
            existing_answer = Answer.query()\
                .filter_by(case=session_id, answeredquestion=question_obj.id)\
                .first()
            if existing_answer:
                existing_answer.update(answer=answer_data)
            else:
                Answer.create(answer=answer_data, case=session_id,
                    answeredquestion=question_obj.id)
        return redirect(url_for("questions.question",
            question_id=question_id+1))
    return render_template('form.html', form=form,
        question_group=question_group, question_fields=question_fields)


# Route for advice page
@bp.route('/advice', methods=['GET', 'POST'])
def advice():
    # Checks whether there is a session_id, otherwise the user gets redirected
    # to the startpage
    session_id = request.cookies.get('sessionID')
    if not session_id:
        redirect(url_for('main.index'))
    case = Case.query().filter_by(id=session_id).first()
    if not case:
        redirect(url_for('main.index'))

    
    # Collect the answers, questions, and groups
    groups_dict = {"groups": []}
    for answer in case.answer_case.all():
        question = answer.answered_question
        group = question.belongs_to_groups.first()
        if f"group-{group.id}" in groups_dict["groups"]:
            groups_dict[f"group-{group.id}"]["questions"].append({
                "question": question,
                "answer": answer
            })
        else:
            groups_dict["groups"].append(f"group-{group.id}")
            groups_dict[f"group-{group.id}"] = {
                "group": group,
                "questions": [{
                    "question": question,
                    "answer": answer
                }]

            }

    form = EmailForm()
    answers_list = []
    for answer in case.answer_case.all():
        answers_list.append((answer.answered_question.question, answer.answer),)
    generate_report(answers_list, session_id)
    if form.validate_on_submit():
        email_address = [form.answer.data]
        send_email('Data en wat nu rapport', current_app.config['ADMINS'][0], email_address, 'In de bijlage treft u het Data en wat nu rapport aan.', 'In de bijlage treft u het Data en wat nu rapport aan.', session_id)
    return render_template('advice.html', extra_text="Dit is de eindpagina", 
        title="Eindpagina", form=EmailForm(), groups_dict=groups_dict)

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