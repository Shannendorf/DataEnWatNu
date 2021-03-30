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
    q1 = Question.create(question="Databeheer (kwaliteit, toegankelijkheid en vindbaarheid) wordt belangrijk gevonden en krijgt structureel aandacht.", questiontype="likert", weight=10)
    q2 = Question.create(question="Het werken met data wordt gezien als een activiteit die kosten kan besparen.", questiontype="likert", weight=20)
    q3 = Question.create(question="Mijn concurrenten investeren in het creëren van toegevoegde waarde met data.", questiontype="likert", weight=30)
    q4 = Question.create(question="Slim gebruik maken van data past binnen mijn organisatie.", questiontype="likert", weight=40)
    q5 = Question.create(question="We zijn bereid tijd, geld en denkkracht te stoppen in het creëren van toegevoegde waarde met data.", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Binnen uw organisatie is er geen gevoel van urgentie om aan de slag te gaan met het creëren van toegevoegde waarde met data.", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Binnen uw organisatie is er een laag gevoel van urgentie om aan de slag te gaan met het creëren van toegevoegde waarde met data.", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Binnen uw organisatie is er een middelmatig gevoel van urgentie om aan de slag te gaan met het creëren van toegevoegde waarde met data.", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Binnen uw organisatie is er een hoog gevoel van urgentie om aan de slag te gaan met het creëren van toegevoegde waarde met data.", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_2():
    group = QuestionGroup.create(title="Data op strategisch niveau", group_type="likert", weight=10)
    q1 = Question.create(question="Wij vinden het belangrijk om de juiste data op het juiste moment bij de juiste persoon te krijgen.", questiontype="likert", weight=10)
    q2 = Question.create(question="We sturen actief op het creëren van toegevoegde waarde met data en gebruiken de inzichten om ons beleid hierop aan te passen.", questiontype="likert", weight=20)
    q3 = Question.create(question="Het werken met data wordt gezien als kostenpost, niet als investering.", questiontype="likert", weight=30, reversed_score=True)
    q4 = Question.create(question="Werken met data wordt niet gezien als integraal onderdeel van de strategische, tactische en operationele sturing.", questiontype="likert", weight=40, reversed_score=True)
    q5 = Question.create(question="Het leiderschap binnen de organisatie ondersteunt en promoot het gebruik van data.", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Op strategisch niveau wordt niet of nauwelijks gestuurd op basis van data. Daarnaast wordt op strategisch niveau niet of nauwelijks geïnvesteerd in het creëren van toegevoegde waarde met data.", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Op strategisch niveau wordt niet structureel gestuurd op basis van data. Daarnaast wordt op strategisch niveau nauwelijks geïnvesteerd in het creëren van toegevoegde waarde met data.", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Op strategisch niveau wordt gestuurd op basis van data. Daarnaast wordt op strategisch niveau structureel geïnvesteerd in het creëren van toegevoegde waarde met data.", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Data is een integraal onderdeel van de strategie en wordt gebruikt om zowel strategisch, tactisch als operationeel het beleid aan te passen.", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_3():
    group = QuestionGroup.create(title="Skillset medewerkers", group_type="likert", weight=10)
    q1 = Question.create(question="Minimaal één medewerker, waarvan de dagelijkse werkzaamheden volledig bestaan uit het creëren van toegevoegde waarde met data.", questiontype="likert", weight=10)
    q2 = Question.create(question="We hebben niet de kennis in huis om te analyseren hoe we presteren op basis van data.", questiontype="likert", weight=20, reversed_score=True)
    q3 = Question.create(question="We hebben de kennis in huis om toegevoegde waarde te creëren met voorspellende modellen en algoritmen.", questiontype="likert", weight=30)
    q4 = Question.create(question="De medewerkers zijn in staat om data uit meerdere bronnen te koppelen om hieruit informatie, kennis en toegevoegde waarde te halen.", questiontype="likert", weight=40)
    q5 = Question.create(question="De medewerkers zijn in staat om vraagstukken te identificeren die ze kunnen beantwoorden met behulp van data.", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Uw medewerkers zijn op dit moment in bredere zin niet vaardig genoeg om toegevoegde waarde te creëren met data.", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Uw medewerkers zijn op dit moment niet op alle gebieden vaardig genoeg om toegevoegde waarde te creëren met data.", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Uw organisatie heeft voldoende kwaliteiten in huis om toegevoegde waarde te creëren met data.", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="U heeft alle kwaliteiten in huis om vraagstukken te identificeren en toegevoegde waarde te creëren met data.", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_4():
    group = QuestionGroup.create(title="Staat van digitalisering", group_type="likert", weight=10)
    q1 = Question.create(question="In onze organisatie is iedereen zich bewust van de toegevoegde waarde van data.", questiontype="likert", weight=10)
    q2 = Question.create(question="In onze organisatie, is data toegankelijk, kwalitatief goed en vindbaar.", questiontype="likert", weight=20)
    q3 = Question.create(question="Databeheer (kwaliteit, toegankelijkheid en vindbaarheid) wordt ingevuld door individuen en losstaande initiatieven.", questiontype="likert", weight=30, reversed_score=True)
    q4 = Question.create(question="Het verzamelen, opslaan, bewerken en mogelijk analyseren van de data gebeurt nog voor een deel op papier.", questiontype="likert", weight=40, reversed_score=True)
    q5 = Question.create(question="We werken met losse systemen die niet aan elkaar gekoppeld zijn en niet specifiek bedoeld zijn om te werken met data.", questiontype="likert", weight=50, reversed_score=True)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="In uw organisatie is de data niet toegankelijk, kwalitatief slecht en niet vindbaar. Er wordt gewerkt met losse systemen die niet aan elkaar gekoppeld zijn.", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="In uw organisatie is de data beperkt toegankelijk, kwalitatief niet goed en slecht vindbaar. Er wordt gewerkt met losse systemen die nauwelijks aan elkaar gekoppeld zijn.", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="In uw organisatie is de data in de meeste gevallen toegankelijk, kwalitatief goed en vindbaar. Systemen worden aan elkaar gekoppeld om meer toegevoegde waarde uit de data te halen.", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="In uw organisatie is de data toegankelijk, kwalitatief goed en vindbaar. Systemen zijn aan elkaar gekoppeld en iedereen is zich bewust van de toegevoegde waarde van data.", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
    return group


def create_question_group_5():
    group = QuestionGroup.create(title="Bereidheid tot verandering", group_type="likert", weight=10)
    q1 = Question.create(question="We hebben het gevoel dat we beter inzicht zouden kunnen krijgen in de verzamelde data.", questiontype="likert", weight=10)
    q2 = Question.create(question="In onze organisatie is er weinig vertrouwen in de kwaliteit, toegankelijkheid en vindbaarheid van de data.", questiontype="likert", weight=20, reversed_score=True)
    q3 = Question.create(question="Er is een cultuur van innovatie in uw bedrijf die zich leent voor het creëren van toegevoegde waarde met data.", questiontype="likert", weight=30)
    q4 = Question.create(question="Ons personeel voelt zich prettig bij meer digitalisering.", questiontype="likert", weight=40)
    q5 = Question.create(question="Ons personeel is bereid zich nieuwe tools eigen te maken.", questiontype="likert", weight=50)
    group.add_question(q1)
    group.add_question(q2)
    group.add_question(q3)
    group.add_question(q4)
    group.add_question(q5)
    add_group_options(group)
    ScoreText.create(text="Binnen uw organisatie is op dit moment geen bereidheid tot verandering.", lower_limit=4.9, upper_limit=8.1, weight=10, group=group.id)
    ScoreText.create(text="Binnen uw organisatie is op dit moment weinig bereidheid tot verandering.", lower_limit=8.9, upper_limit=12.1, weight=10, group=group.id)
    ScoreText.create(text="Binnen uw organisatie is op dit moment bereidheid tot verandering.", lower_limit=12.9, upper_limit=16.1, weight=10, group=group.id)
    ScoreText.create(text="Binnen uw organisatie is op dit moment een gezonde voedingsbodem voor verandering en innovatie.", lower_limit=16.9, upper_limit=20.1, weight=10, group=group.id)
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
