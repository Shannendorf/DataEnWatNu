# Models
from datetime import datetime
from typing import Type
from sqlalchemy import Column, Integer, String, Text, ARRAY, ForeignKey, \
    DateTime, Table, Boolean, and_, Float
from sqlalchemy.orm import backref, relationship
from secrets import token_urlsafe

from src.database import Model


QuestionGroupQuestion = Table(
    'QuestionGroupQuestion',
    Model.metadata,
    Column('question_group_id', Integer, ForeignKey('QuestionGroup.id')),
    Column('question_id', Integer, ForeignKey('Question.id'))
)

QuestionListQuestionGroup = Table(
    "QuestionListQuestionGroup",
    Model.metadata,
    Column("question_list_id", Integer, ForeignKey("QuestionList.id")),
    Column("question_group_id", Integer, ForeignKey("QuestionGroup.id"))
)


class QuestionType(Model):
    __tablename__ = 'QuestionType'

    name = Column(String(128), primary_key=True)
    function = Column(String(128))
    form = Column(String(128))

    type_question = relationship('Question', backref='question_type',
        lazy='dynamic')


class Question(Model):
    __tablename__ = 'Question'
    
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    options = Column(ARRAY(String))
    weight = Column(Integer)
    reversed_score = Column(Boolean, default=False)
    questiontype = Column(String(64), ForeignKey('QuestionType.name'))

    answer_question = relationship('Answer', backref='answered_question',
        lazy='dynamic')
    groups = relationship(
        'QuestionGroup', secondary=QuestionGroupQuestion,
        primaryjoin=(QuestionGroupQuestion.c.question_id == id),
        backref=backref('group_questions', lazy='dynamic'), lazy='dynamic')


class Answer(Model):
    __tablename__ = 'Answer'

    answeredquestion = Column(Integer, ForeignKey('Question.id'),
        primary_key=True)
    answer = Column(String(256))
    case = Column(String, ForeignKey('Case.id'), primary_key=True)
    group = Column(Integer, ForeignKey("QuestionGroup.id"))

    def format_answer(self):
        if self.answer_group.group_type == "likert":
            option = LikertOption.query()\
                .filter(and_(
                    LikertOption.group_id == self.group,
                    LikertOption.value == int(self.answer)))\
                .first()
            return f"{option.text} ({option.value})"
        return self.answer


class LikertOption(Model):
    __tablename__ = "LikertOption"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    value = Column(Integer)
    weight = Column(Integer)
    group_id = Column(Integer, ForeignKey("QuestionGroup.id"))


class QuestionGroup(Model):
    __tablename__ = 'QuestionGroup'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    group_type = Column(String)
    description = Column(Text)
    weight = Column(Integer)

    likert_options = relationship("LikertOption", backref="likert_group",
        lazy="dynamic")
    answers = relationship("Answer", backref="answer_group", lazy="dynamic")
    texts = relationship("ScoreText", backref="text_group", lazy="dynamic")

    questions = relationship(
        'Question', secondary=QuestionGroupQuestion,
        primaryjoin=(QuestionGroupQuestion.c.question_group_id == id),
        backref=backref('belongs_to_groups', lazy='dynamic'),
        lazy='dynamic')
    lists = relationship(
        "QuestionList", secondary=QuestionListQuestionGroup,
        primaryjoin=(QuestionListQuestionGroup.c.question_group_id == id),
        backref=backref("list_groups", lazy="dynamic"), lazy="dynamic")

    def add_question(self, question):
        if self.group_type != "other" and question.questiontype != self.group_type:
            raise RuntimeError(f"QuestionGroup of type {self.group_type} " +
                f"cannot contain questions of type {question.questiontype}")
        self.questions.append(question)
        self.save()

    def add_likert_option(self, option):
        if self.group_type != "likert":
            raise RuntimeError("Cannot add likert option to group with " +
                f"type {self.group_type}")
        self.likert_options.append(option)
        self.save()

    def calculate_score_for_case(self, case):
        if self.group_type != "likert":
            return 0
        options = self.likert_options.order_by(LikertOption.weight).all()
        values = [o.value for o in options]

        total = 0
        count = 0
        for question in self.questions.all():
            answer = Answer.query().filter(and_(
                Answer.answeredquestion == question.id,
                Answer.case == case.id
            )).first()
            value = int(answer.answer)
            if answer.answered_question.reversed_score:
                index = values.index(value)
                value = values[-index-1]
            total += value
            count += 1
        return total

    def get_texts(self, score):
        return self.texts.filter(and_(ScoreText.lower_limit<=score,
            ScoreText.upper_limit>=score)).order_by(ScoreText.weight).all()
        

class Case(Model):
    __tablename__ = 'Case'

    id = Column(String, primary_key=True)
    start = Column(DateTime, index=True, default=datetime.utcnow())
    company = Column(String, index=True)
    email = Column(String)
    branch = Column(String)
    company_size = Column(String)
    participant_function = Column(String)
    code_used = Column(Integer, ForeignKey("Code.id"))
    list_selected = Column(Integer, ForeignKey("QuestionList.id"))

    answer_case = relationship('Answer', backref='sessioncase', lazy='dynamic')

    @classmethod
    def create_case(cls, code_used):
        c_id = token_urlsafe(128)
        while cls.query().filter_by(id=c_id).with_entities(cls.id).count() != 0:
            c_id = token_urlsafe(128)
        return cls.create(id=c_id, code_used=code_used.id)


class Code(Model):
    __tablename__ = "Code"

    id = Column(Integer, primary_key=True)
    code = Column(String, index=True)
    create_on = Column(DateTime, default=datetime.utcnow())
    active = Column(Boolean)

    cases = relationship("Case", backref="case_code", lazy="dynamic")

    @classmethod
    def get_code(cls, code):
        return cls.query().filter_by(code=code).first()
        


class QuestionList(Model):
    __tablename__ = "QuestionList"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    
    cases = relationship("Case", backref="case_list", lazy="dynamic")

    groups = relationship(
        "QuestionGroup", secondary=QuestionListQuestionGroup,
        primaryjoin=(QuestionListQuestionGroup.c.question_list_id == id),
        backref=backref("group_lists", lazy="dynamic"), lazy="dynamic")

    def add_group(self, group):
        if type(group) == int:
            group = QuestionGroup.get_by_id(group)
        if not group:
            raise RuntimeError("QuestionGroup not found")
        if type(group) != QuestionGroup:
            raise TypeError(
                f"Expected QuestionGroup object, got {type(group)}")
        if group not in self.groups.all():
            self.groups.append(group)
            self.save()

    def add_groups(self, groups):
        for group in groups:
            self.add_group(group)


class ScoreText(Model):
    __tablename__ = "ScoreText"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    lower_limit = Column(Float)
    upper_limit = Column(Float)
    weight = Column(Integer)
    group = Column(Integer, ForeignKey("QuestionGroup.id"))