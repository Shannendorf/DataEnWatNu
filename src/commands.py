from flask.cli import FlaskGroup
from secrets import token_urlsafe

from src.app import create_app
from src.database import db
from src.models import QuestionType, Question, QuestionGroup

cli = FlaskGroup(create_app=create_app)
app = create_app()


@cli.command()
def drop_db():
    db.drop_all()
    db.session.commit()


# Generates and adds basic testdata to db
@cli.command()
def generate_testdata():
    QuestionType.create(name='open', form='OpenQuestionForm')
    QuestionType.create(name="multiplechoice", form="MCQuestionForm")
    
    qg1 = QuestionGroup.create(title="Group 1", description="This is the first group", group_type="other")
    q1 = Question.create(question="Wat is uw functie binnen het bedrijf/de organisatie waar u werkzaam bent?", questiontype="open")
    q2 = Question.create(question="Werkt u binnen uw functie vaak met data?", questiontype="open")    
    q3 = Question.create(question="Heeft u in het verleden een beroepsfunctie gehad waarbinnen u met data heeft gewerkt?", questiontype="open")
    q4 = Question.create(question="Welke optie kiest u?", questiontype="multiplechoice", options={"optie 1", "optie 2", "optie 3"})
    qg1.add_question(q1)
    qg1.add_question(q2)
    qg1.add_question(q3)
    qg1.add_question(q4)

    db.session.commit()