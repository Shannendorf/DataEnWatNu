from flask.cli import FlaskGroup
from secrets import token_urlsafe
from sqlalchemy import MetaData

from src.app import create_app
from src.database import db
from src.models import LikertOption, QuestionList, QuestionType, Question, \
    QuestionGroup, Code, ScoreText

cli = FlaskGroup(create_app=create_app)
app = create_app()


@cli.command()
def drop_db():
    if db.engine.has_table("alembic_version"):
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS alembic_version")
        conn.commit()
        cursor.close()
    db.drop_all()
    db.session.commit()


# Generates and adds basic testdata to db
@cli.command()
def generate_testdata():
    QuestionType.create(name='open', form='OpenQuestionForm')
    QuestionType.create(name="multiplechoice", form="MCQuestionForm")
    QuestionType.create(name="likert")
    
    qg1 = QuestionGroup.create(title="Group 1", description="This is the first group", group_type="other", weight=50)
    q1 = Question.create(question="Wat is uw functie binnen het bedrijf/de organisatie waar u werkzaam bent?", questiontype="open", weight=10)
    q2 = Question.create(question="Werkt u binnen uw functie vaak met data?", questiontype="open", weight=20)    
    q3 = Question.create(question="Heeft u in het verleden een beroepsfunctie gehad waarbinnen u met data heeft gewerkt?", questiontype="open", weight=30)
    q4 = Question.create(question="Welke optie kiest u?", questiontype="multiplechoice", options=["optie 1", "optie 2", "optie 3"], weight=5)
    qg1.add_question(q1)
    qg1.add_question(q2)
    qg1.add_question(q3)
    qg1.add_question(q4)

    qg2 = QuestionGroup.create(title="Group 2", description="This is the second group (a likert group)", group_type="likert", weight=40)
    lo1 = LikertOption.create(text="Helemaal Oneens", weight=1, value=1)
    lo2 = LikertOption.create(text="Oneens", weight=2, value=2)
    lo3 = LikertOption.create(text="Neutraa", weight=3, value=3)
    lo4 = LikertOption.create(text="Eens", weight=4, value=4)
    lo5 = LikertOption.create(text="Helemaal Eens", weight=5, value=5)
    qg2.add_likert_option(lo1)
    qg2.add_likert_option(lo2)
    qg2.add_likert_option(lo3)
    qg2.add_likert_option(lo4)
    qg2.add_likert_option(lo5)
    q2_1 = Question.create(question="First likert", questiontype="likert", options=["eens", "neutraal", "oneens"], weight=10)
    q2_2 = Question.create(question="Second likert", questiontype="likert", options=["eens", "neutraal", "oneens"], weight=5)
    q2_3 = Question.create(question="Third likert", questiontype="likert", options=["eens", "neutraal", "oneens"], weight=20, reversed_score=True)
    qg2.add_question(q2_1)
    qg2.add_question(q2_2)
    qg2.add_question(q2_3)
    st1 = ScoreText.create(text="Low score", lower_limit=0, upper_limit=1.5, weight=10, group=qg2.id)
    st2 = ScoreText.create(text="Medium score", lower_limit=1.51, upper_limit=3, weight=20, group=qg2.id)
    st3 = ScoreText.create(text="High score", lower_limit=3.001, upper_limit=6, weight=30, group=qg2.id)
    st4 = ScoreText.create(text="Overlapping text", lower_limit=0, upper_limit=6, weight=5, group=qg2.id)
    st5 = ScoreText.create(lower_limit=0, upper_limit=6, weight=100, group=qg2.id, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris volutpat nec arcu sit amet venenatis. Sed sagittis tortor ut risus consequat feugiat. Pellentesque vestibulum nibh non leo ultrices tristique. Donec porttitor at nisl ut sagittis. In a volutpat libero. Nullam vel orci euismod enim dignissim lacinia sed nec mi. Curabitur sodales lobortis leo quis fermentum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean rutrum sodales ultrices. Nunc lobortis ultrices commodo. Morbi iaculis metus vel elit malesuada, ullamcorper malesuada metus viverra. Nunc nec ex varius, varius eros eget, aliquet purus. ")


    qg3 = QuestionGroup.create(title="Group 3", description="This is the third group", group_type="other", weight=60)
    q3_1 = Question.create(question="Question one", questiontype="open", weight=10)
    q3_2 = Question.create(question="Question two", questiontype="open", weight=20)
    qg3.add_question(q3_1)
    qg3.add_question(q3_2)

    ql1 = QuestionList.create(name="Question List 1")
    ql1.add_groups([qg1, qg2, qg3])

    ql2 = QuestionList.create(name="Question List 2")
    ql2.add_groups([qg1, qg3])

    code = Code.create(code="aabb", active=True)

    db.session.commit()