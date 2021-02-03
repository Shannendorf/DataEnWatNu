from flask.cli import FlaskGroup
from secrets import token_urlsafe

from src.app import create_app
from src.database import db
from src.models import QuestionType, Question

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
    Question.create(question="Wat is uw functie binnen het bedrijf/de organisatie waar u werkzaam bent?", questiontype="open")
    Question.create(question="Werkt u binnen uw functie vaak met data?", questiontype="open")    
    Question.create(question="Heeft u in het verleden een beroepsfunctie gehad waarbinnen u met data heeft gewerkt?", questiontype="open")
    Question.create(question="Welke optie kiest u?", questiontype="multiplechoice", options={"optie 1", "optie 2", "optie 3"})
    db.session.commit()