from typing import List
import pytest
from datetime import datetime, timedelta

from src.models import Case, Code, LikertOption, Question, Answer, QuestionGroup, \
    QuestionList, QuestionType, ScoreText


@pytest.fixture
def case(app) -> Case:
    return Case.create(
        id="TestCase1",
        start=datetime.utcnow() - timedelta(minutes=5),
        company="Testing Company",
        email="test@testing-company.com",
        branch="Testing",
        company_size=42,
        participant_function="Tester",
    )


@pytest.fixture
def likert_options(likert_question_group):
    options = []
    for i in range(1, 6):
        options.append(LikertOption.create(
            text=f"Test option {i}",
            value=i,
            weight=i,
            group_id=likert_question_group.id
        ))
    return options


@pytest.fixture
def likert_question_type(app) -> QuestionType:
    return QuestionType.create(name="likert")


@pytest.fixture
def likert_question_group(likert_question_type) -> QuestionGroup:
    return QuestionGroup.create(title="Test Group", group_type="likert",
        weight=5, description="This is a test question group")


@pytest.fixture
def likert_question(likert_question_group, likert_question_type) -> Question:
    q = Question.create(question="Test Question", weight=5,
        options=[1, 2, 3, 4], questiontype=likert_question_type.name)
    q.groups.append(likert_question_group)
    q.save()
    return q


@pytest.fixture
def likert_answer(case, likert_question, likert_question_group,
        likert_options) -> Answer:
    return Answer.create(
        answeredquestion=likert_question.id,
        answer=likert_options[1].value,
        case=case.id,
        group=likert_question_group.id
    )


@pytest.fixture
def open_question_type(app) -> QuestionType:
    return QuestionType.create(name="open")


@pytest.fixture
def open_question_group(open_question_type) -> QuestionGroup:
    return QuestionGroup.create(
        title="Open Test Group",
        group_type="open",
        weight=3,
        description="This is an open question group"
    )


@pytest.fixture
def open_question(open_question_group, open_question_type) -> Question:
    q = Question.create(question="Test Question", weight=5,
        options=[1, 2, 3, 4], questiontype=open_question_type.name)
    q.groups.append(open_question_group)
    q.save()
    return q


@pytest.fixture
def open_answer(case, open_question, open_question_group) -> Answer:
    return Answer.create(
        answeredquestion=open_question.id,
        answer="Some answer",
        case=case.id,
        group=open_question_group.id
    )


@pytest.fixture
def open_question_not_linked(open_question_type) -> Question:
    return Question.create(
        question="Test question",
        weight=5,
        options=[1, 2, 3, 4],
        questiontype=open_question_type.name
    )


@pytest.fixture
def score_texts(likert_question_group) -> List[ScoreText]:
    texts = [
        ScoreText.create(text="text1", upper_limit=2.1, lower_limit=0,
            weight=1, group=likert_question_group.id),
        ScoreText.create(text="text2", upper_limit=4.1, lower_limit=2.1,
            weight=1, group=likert_question_group.id),
        ScoreText.create(text="text3", upper_limit=4.1, lower_limit=5.1,
            weight=1, group=likert_question_group.id)
    ]
    return texts


@pytest.fixture
def code(app) -> Code:
    return Code.create(code="TESTCODE", active=True)


@pytest.fixture
def question_list(app) -> QuestionList:
    return QuestionList.create(name="Test List")


@pytest.fixture
def question_lists(question_list) -> List[QuestionList]:
    lists = [question_list]
    for i in range(2, 5):
        lists.append(QuestionList.create(name=f"Test List {i}"))
    return lists
