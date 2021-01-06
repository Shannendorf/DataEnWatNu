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
    Question.create(question="Wat is uw functie binnen het bedrijf/de organisatie waar u werkzaam bent?", questiontype="open")
    Question.create(question="Werkt u binnen uw functie vaak met data?", questiontype="open")    
    Question.create(question="Heeft u in het verleden een beroepsfunctie gehad waarbinnen u met data heeft gewerkt?", questiontype="open")   
    db.session.commit()