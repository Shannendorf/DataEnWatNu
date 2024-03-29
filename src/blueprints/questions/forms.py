# Forms for the questions module
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField,\
    BooleanField, RadioField
from wtforms.validators import DataRequired, Email

from src.models import LikertOption, Question


def QuestionnaireForm(question_group, include_submit = True, submit_text = ""):
    class BaseForm(FlaskForm):
        pass

    question_ids = {}
    likert_options = question_group.likert_options\
        .order_by(LikertOption.weight).all()
    for i, question in enumerate(question_group.questions\
            .order_by(Question.weight).all()):
        question_id = f"q{i}"
        question_ids[question_id] = question
        required_msg = "Dit veld is verplicht"

        if question.questiontype == "likert":
            setattr(BaseForm, question_id, RadioField(question.question,
                choices=[(o.value, o.text) for o in likert_options],
                validators=[DataRequired(message=required_msg)]))
        elif question.questiontype == "open":
            setattr(BaseForm, question_id,
                StringField(question.question, validators=[DataRequired(message=required_msg)]))
        elif question.questiontype == "integer":
            setattr(BaseForm, question_id,
                IntegerField(question.question, validators=[DataRequired(message=required_msg)]))
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


# Form for questions that require an email adress input
class EmailForm(FlaskForm):
    answer = StringField('Voer hier uw e-mailadres in als u het rapport toegestuurd wilt krijgen.', validators=[Email(), DataRequired()])
    submit = SubmitField('Bevestig')


class LoginForm(FlaskForm):
    code = StringField("Login code", validators=[DataRequired(message="Dit veld is verplicht")])
    submit = SubmitField("Akkoord en verder")


branch_options = [
    "Activiteiten van extraterritoriale organisaties en lichamen",
    "Landbouw, bosbouw en visserij",
    "Mijnbouw en steengroeven",
    "Productie",
    "Elektriciteit, gas, stroom en airconditioning",
    "Watervoorziening, riolering, afvalbeheer en saneringsactiviteiten",
    "Constructie",
    "Groot- en detailhandel, reparatie van motervoertuigen en motorfietsen",
    "Transport en opslag",
    "Accommodatie en maaltijden",
    "Informatie en communicatie",
    "Financiële en verzekeringsactiviteiten",
    "Vastgoedactiviteiten",
    "Professionele, wetenschappelijke en technische activiteiten",
    "Administratieve en ondersteunende activiteiten",
    "Openbaar bestuur en defensie, verplichte sociale zekerheid",
    "Onderwijs",
    "Menselijke gezondheid en sociale activiteiten",
    "Kust, amusement en recreatie",
    "Overige dienstenacitiveiten",
    "Huishoudens als werkgever, ongedifferentieerde goederen- en diensten, producerende activiteiten"
]


class IntroFormNoListSelection(FlaskForm):
    has_selection = False
    company = StringField("Bedrijfsnaam", validators=[DataRequired(message="Dit veld is verplicht")])
    email = StringField("Email", validators=[DataRequired(message="Dit veld is verplicht"), Email(message="Geen valide e-mailadres")])
    branch = SelectField("Bedrijfsbranch", choices=branch_options)
    company_size = StringField("Bedrijfsgrootte", validators=[DataRequired(message="Dit veld is verplicht")])
    participant_function = StringField("Uw functie", validators=[DataRequired(message="Dit veld is verplicht")])
    submit = SubmitField("Start vragenlijst")


class IntroForm(FlaskForm):
    has_selection = True
    company = StringField("Bedrijfsnaam", validators=[DataRequired(message="Dit veld is verplicht")])
    email = StringField("Email", validators=[DataRequired(message="Dit veld is verplicht"), Email(message="Geen valide e-mailadres")])
    branch = SelectField("Bedrijfsbranch", choices=branch_options)
    company_size = StringField("Bedrijfsgrootte", validators=[DataRequired(message="Dit veld is verplicht")])
    participant_function = StringField("Uw functie", validators=[DataRequired(message="Dit veld is verplicht")])
    selection = SelectField("Select one")
    submit = SubmitField("Select")
