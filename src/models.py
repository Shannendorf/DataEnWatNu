# Models

from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from secrets import token_urlsafe

from src.database import Model


class QuestionType(Model):
    __tablename__ = 'QuestionType'

    name = Column(String(128), primary_key=True)
    function = Column(String(128))
    form = Column(String(128))

    type_question = relationship('Question', backref='question_type', lazy='dynamic')


class Question(Model):
    __tablename__ = 'Question'
    
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    options = Column(ARRAY(String))
    questiontype = Column(String(64), ForeignKey('QuestionType.name'))

    answer_question = relationship('Answer', backref='answered_question', lazy='dynamic')


class Answer(Model):
    __tablename__ = 'Answer'

    answeredquestion = Column(Integer, ForeignKey('Question.id'), primary_key=True)
    answer = Column(String(256))
    case = Column(String, ForeignKey('Case.id'), primary_key=True)


class Case(Model):
    __tablename__ = 'Case'

    id = Column(String, primary_key=True)
    start = Column(DateTime)

    answer_case = relationship('Answer', backref='sessioncase', lazy='dynamic')

    @classmethod
    def create_case(cls):
        c_id = token_urlsafe(128)
        while cls.query().filter_by(id=c_id).with_entities(cls.id).count() != 0:
            c_id = token_urlsafe(128)
        return cls.create(id=c_id)