# Forms for the questions module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email


def QuestionnaireForm(question_group, include_submit = True, submit_text = ""):
    class BaseForm(FlaskForm):
        pass

    question_ids = {}
    for i, question in enumerate(question_group.questions.all()):
        question_id = f"q{i}"
        question_ids[question_id] = question

        if question.questiontype == "likert":
            setattr(BaseForm, question_id, RadioField(question.question,
                choices=list(question.options)))
        elif question.questiontype == "open":
            setattr(BaseForm, question_id,
                StringField(question.question, validators=[DataRequired()]))
        elif question.questiontype == "integer":
            setattr(BaseForm, question_id,
                IntegerField(question.question, validators=[DataRequired()]))
        elif question.questiontype == "bool":
            setattr(BaseForm, question_id, BooleanField(question.question))
        elif question.questiontype == "multiplechoice":
            setattr(BaseForm, question_id, SelectField(question.question,
                choices=list(question.options)))
        else:
            raise RuntimeError(f"Question type {question.questiontype} " +
                "not supported")

    if include_submit:
        BaseForm.submit = SubmitField(submit_text)

    return (BaseForm(), question_ids)


# Form for open question
class OpenQuestionForm(FlaskForm):
    answer = StringField(validators=[DataRequired()])
    submit = SubmitField('Bevestig')


# Form for questions with an integer answer
class IntQuestionForm(FlaskForm):
    answer = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Bevestig')


# Form for questions with a boolean answer
class BoolQuestionForm(FlaskForm):
    answer = BooleanField()
    submit = SubmitField('Bevestig')


# Form for questions with a multiple choice answer
class MCQuestionForm(FlaskForm):
    answer = SelectField('Selecteer een optie')
    submit = SubmitField('Bevestig')


# Form for Likert questions
class LikertQuestionForm(FlaskForm):
    nr = 0
    answer = RadioField(choices=["option1", "option2", "option3"])
    answer2 = RadioField()
    answer3 = RadioField()
    answer4 = RadioField()
    answer5 = RadioField()
    submit = SubmitField('Bevestig')


# Form for questions that require an email adress input
class EmailForm(FlaskForm):
    answer = StringField('Voer hier uw e-mailadres in als u het rapport toegestuurd wilt krijgen.', validators=[Email(), DataRequired()])
    submit = SubmitField('Bevestig')


string_to_form = {
    "open" : OpenQuestionForm,
    "multiplechoice" : MCQuestionForm,
    "bool" : BoolQuestionForm,
    "likert" : LikertQuestionForm
}

def get_form(formtype):
    return string_to_form[formtype]()


class LoginForm(FlaskForm):
    code = StringField("Login code", validators=[DataRequired()])
    submit = SubmitField("Login")
