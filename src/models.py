# Models
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey, \
    DateTime, Table, Boolean
from sqlalchemy.orm import backref, relationship
from secrets import token_urlsafe

from src.database import Model


QuestionGroupQuestion = Table(
    'QuestionGroupQuestion',
    Model.metadata,
    Column('question_group_id', Integer, ForeignKey('QuestionGroup.id')),
    Column('question_id', Integer, ForeignKey('Question.id'))
)


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
    groups = relationship(
        'QuestionGroup', secondary=QuestionGroupQuestion,
        primaryjoin=(QuestionGroupQuestion.c.question_id == id),
        backref=backref('group_questions', lazy='dynamic'),
        lazy='dynamic'
    )


class Answer(Model):
    __tablename__ = 'Answer'

    answeredquestion = Column(Integer, ForeignKey('Question.id'), primary_key=True)
    answer = Column(String(256))
    case = Column(String, ForeignKey('Case.id'), primary_key=True)


class QuestionGroup(Model):
    __tablename__ = 'QuestionGroup'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    group_type = Column(String)
    description = Column(Text)
    questions = relationship(
        'Question', secondary=QuestionGroupQuestion,
        primaryjoin=(QuestionGroupQuestion.c.question_group_id == id),
        backref=backref('belongs_to_groups', lazy='dynamic'),
        lazy='dynamic'
    )

    def add_question(self, question):
        if self.group_type != "other" and question.questiontype != self.group_type:
            raise RuntimeError(f"QuestionGroup of type {self.group_type} " +
                f"cannot contain questions of type {question.questiontype}")
        self.questions.append(question)
        self.save()


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


class Code(Model):
    __tablename__ = "Code"

    id = Column(Integer, primary_key=True)
    code = Column(String, index=True)
    create_on = Column(DateTime, default=datetime.utcnow())
    active = Column(Boolean)

    @classmethod
    def check_code(cls, code):
        return bool(cls.query().filter_by(code=code).first())
