# Models

from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database import Model


class QuestionType(Model):
    __tablename__ = 'QuestionType'

    name = Column(String(128), primary_key=True)
    function = Column(String(128))
    form = Column(String(128))

    type_question = relationship('Question', backref='questiontype', lazy='dynamic')


class Question(Model):
    __tablename__ = 'Question'
    
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    options = Column(ARRAY(String))
    questiontype = Column(String(64), ForeignKey('QuestionType.name'))

    answer_question = relationship('Answer', backref='answeredquestion', lazy='dynamic')


class Answer(Model):
    __tablename__ = 'Answer'

    answeredquestion = Column(Integer, ForeignKey('Question.id'), primary_key=True)
    answer = Column(String(256))
    case = Column(Integer, ForeignKey('Case.id'))


class Case(Model):
    __tablename__ = 'Case'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)

    answer_case = relationship('Answer', backref='case', lazy='dynamic')
