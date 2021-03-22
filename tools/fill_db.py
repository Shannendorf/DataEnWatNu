import os, sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path)


from src.app import create_app 
from src.database import db
from src.models import QuestionList, QuestionType, Question, QuestionGroup, \
    Code, ScoreText, LikertOption


def create_question_types():
    QuestionType.create(name="likert")


def add_group_options(group):
    group.add_likert_option(LikertOption.create(text="Helemaal oneens", weight=10, value=1))
    group.add_likert_option(LikertOption.create(text="Oneens", weight=20, value=2))
    group.add_likert_option(LikertOption.create(text="Eens", weight=30, value=3))
    group.add_likert_option(LikertOption.create(text="Helemaal eens", weight=40, value=4))


def create_question_group_1():
    group = QuestionGroup.create(title="Gevoel van urgentie", group_type="likert", weight=10)
    q1 = Question.create(question="vraag A1", questiontype="likert", weight=10)
    q2 = Question.create(question="vraag A2", questiontype="likert", weight=20)
    q3 = Question.create(question="vraag A3", questiontype="likert", weight=30)
    q4 = Question.create(question="vraag A4", questiontype="likert", weight=40)
    q5 = Question.create(question="vraag A5", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Tekst voor score: 5-8", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 9-12", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 13-16", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 17-20", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_2():
    group = QuestionGroup.create(title="Data op strategisch niveau", group_type="likert", weight=10)
    q1 = Question.create(question="vraag B1", questiontype="likert", weight=10)
    q2 = Question.create(question="vraag B2", questiontype="likert", weight=20)
    q3 = Question.create(question="vraag B3", questiontype="likert", weight=30)
    q4 = Question.create(question="vraag B4", questiontype="likert", weight=40)
    q5 = Question.create(question="vraag B5", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Tekst voor score: 5-8", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 9-12", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 13-16", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 17-20", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_3():
    group = QuestionGroup.create(title="Skillset medewerkers", group_type="likert", weight=10)
    q1 = Question.create(question="vraag C1", questiontype="likert", weight=10)
    q2 = Question.create(question="vraag C2", questiontype="likert", weight=20)
    q3 = Question.create(question="vraag C3", questiontype="likert", weight=30)
    q4 = Question.create(question="vraag C4", questiontype="likert", weight=40)
    q5 = Question.create(question="vraag C5", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Tekst voor score: 5-8", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 9-12", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 13-16", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 17-20", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_4():
    group = QuestionGroup.create(title="Staat van digitalisering", group_type="likert", weight=10)
    q1 = Question.create(question="vraag D1", questiontype="likert", weight=10)
    q2 = Question.create(question="vraag D2", questiontype="likert", weight=20)
    q3 = Question.create(question="vraag D3", questiontype="likert", weight=30)
    q4 = Question.create(question="vraag D4", questiontype="likert", weight=40)
    q5 = Question.create(question="vraag D5", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Tekst voor score: 5-8", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 9-12", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 13-16", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 17-20", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_5():
    group = QuestionGroup.create(title="Bereidheid tot verandering", group_type="likert", weight=10)
    q1 = Question.create(question="vraag E1", questiontype="likert", weight=10)
    q2 = Question.create(question="vraag E2", questiontype="likert", weight=20)
    q3 = Question.create(question="vraag E3", questiontype="likert", weight=30)
    q4 = Question.create(question="vraag E4", questiontype="likert", weight=40)
    q5 = Question.create(question="vraag E5", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Tekst voor score: 5-8", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 9-12", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 13-16", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Tekst voor score: 17-20", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group



if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_question_types()
        qg1 = create_question_group_1()
        qg2 = create_question_group_2()
        qg3 = create_question_group_3()
        qg4 = create_question_group_4()
        qg5 = create_question_group_5()

        question_list = QuestionList.create(name="DataEnWatNu")
        question_list.add_groups([qg1, qg2, qg3, qg4, qg5])        

        Code.create(code="DataEnWatNu2021", active=True)

        db.session.commit()
