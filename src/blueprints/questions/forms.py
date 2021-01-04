# Forms for the questions module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email


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


# Form for questions that require an email adress input
class EmailForm(FlaskForm):
    answer = StringField('Voer hier uw e-mailadres in als u het rapport toegestuurd wilt krijgen.', validators=[Email()])
    submit = SubmitField('Bevestig')

string_to_form = {
    "open" : OpenQuestionForm
}

def get_form(formtype):
    return string_to_form[formtype]()