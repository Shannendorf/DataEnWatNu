import pytest
from typing import List

from src.models import Answer, Case, Code, LikertOption, Question, \
    QuestionGroup, ScoreText, QuestionList
from tests._fixtures.model_fixtures import open_question_type


class TestAnswerModel:

    def test_format_likert_answer(self, likert_answer: Answer):
        """Test the format answer method with a likert answer."""
        # GIVEN a likert answer
        # WHEN we format the answer
        # THEN a correctly formatted answer is returned
        actual = likert_answer.format_answer()
        assert actual == "Test option 2"

    def test_format_answer(self, open_answer: Answer):
        """Test the format answer method."""
        # GIVEN an answer
        # WHEN we format the answer
        # THEN a correctly formatted answer is returned
        actual = open_answer.format_answer()
        assert actual == open_answer.answer


class TestQuestionGroupModel:

    def test_add_question(self, open_question_group: QuestionGroup,
            open_question_not_linked: Question):
        """Test the add question method."""
        # GIVEN an open question group and an open question
        # WHEN we add the question to the group
        # THEN the question is added to the group
        open_question_group.add_question(open_question_not_linked)
        assert open_question_not_linked.id in [q.id for q in
            open_question_group.questions.all()]

    def test_add_question_type_mismatch(self,
            likert_question_group: QuestionGroup,
            open_question_not_linked: Question):
        """Test the add question method when there is a type mismatch."""
        # GIVEN a likert question group and an open question
        # WHEN we add the question to the group
        # THEN an exception is shown
        with pytest.raises(RuntimeError):
            likert_question_group.add_question(open_question_not_linked)

    def test_add_likert_option(self, likert_options: List[LikertOption],
            likert_question_group: QuestionGroup):
        """Test adding a likert option to a question group."""
        # GIVEN a likert option and a likert group
        # WHEN we add the option to the group
        # THEN the option is added to the group
        likert_question_group.add_likert_option(likert_options[-1])
        assert likert_options[-1].text in [o.text for o in
            likert_question_group.likert_options.all()]
    
    def test_add_likert_option_with_mismatch(self,
            likert_options: List[LikertOption],
            open_question_group: QuestionGroup):
        """Test adding a likert option to a mismatched question group."""
        # GIVEN a likert option and a group with a differnt type
        # WHEN we add the option to the group
        # THEN an exception is thrown
        with pytest.raises(RuntimeError):
            open_question_group.add_likert_option(likert_options[-1])

    def test_calculate_score_for_case(self, case: Case,
            likert_question_group: QuestionGroup,
            likert_options: List[LikertOption],
            likert_answer: Answer):
        """Test the calculate score for a case."""
        # GIVEN a case with ansers and a question group
        # WHEN we request the score
        # THEN the score is calculated
        for option in likert_options:
            likert_question_group.add_likert_option(option)
        actual = likert_question_group.calculate_score_for_case(case)
        assert actual == 2

    def test_calculate_score_for_open_question_group(self, case: Case,
            open_answer: Answer, open_question_group: QuestionGroup):
        """Test the calculate score method with an open question group."""
        # GIVEN a case with answers and a open question group
        # WHEN we request the score
        # THEN 0 is returned
        actual = open_question_group.calculate_score_for_case(case)
        assert actual == 0

    def test_calculate_score_reversed(self, case: Case,
            likert_question_group: QuestionGroup, likert_question: Question,
            likert_options: List[LikertOption], likert_answer: Answer):
        """Test the calculate score method with a reveresed score question."""
        # GIVEN a case with answers and a likert question group
        # WHEN we request the score
        # THEN the score is calculated
        for option in likert_options:
            likert_question_group.add_likert_option(option)
        likert_question.update(reversed_score=True)
        actual = likert_question_group.calculate_score_for_case(case)
        assert actual == 4

    def test_get_text(self, score_texts: List[ScoreText],
            likert_question_group: QuestionGroup):
        """Test the get text method for a question group."""
        # GIVEN some score texts for a question group
        # WHEN we request the text for a score
        # THEN the correct text is returned
        actual = likert_question_group.get_texts(3)
        assert actual == [score_texts[1]]


class TestCaseModel:

    def test_create_case(self, code: Code):
        """Test the create case method."""
        # GIVEN a code
        # WHEN we request to create a case
        # THEN a case is created
        actual = Case.create_case(code)
        assert Case.query().filter_by(id=actual.id).first()


class TestCodeModel:

    def test_get_code(self, code: Code):
        """test the get code method."""
        # GIVEN a code
        # WHEN we request the code
        # THEN the code object is returned
        assert code.id == Code.get_code(code.code).id


class TestQuestionListModel:

    def test_add_group(self, question_list: QuestionList,
            open_question_group: QuestionGroup):
        # GIVEN a question and a question group
        # WHEN we add the group to the question
        # THEN the question is added to the group
        question_list.add_group(open_question_group)
        assert open_question_group.id in [g.id for g in 
            question_list.groups.all()]

    def test_add_group_by_id(self, question_list: QuestionList,
            open_question_group: QuestionGroup):
        # GIVEN a question and a question group
        # WHEN we add the group to the question by ID
        # THEN the question is added to the group
        question_list.add_group(open_question_group.id)
        assert open_question_group.id in [g.id for g in 
            question_list.groups.all()]
    
    def test_add_non_existing_group_by_id(self, question_list: QuestionList):
        # GIVEN a question and a non-existing question group
        # WHEN we add the group to the question by ID
        # THEN a runtime error is thrown
        with pytest.raises(RuntimeError):
            question_list.add_group(42)

    def test_add_group_wrong_type(self, question_list: QuestionList):
        # GIVEN a question and a group with the wrong type
        # WHEN we add the group to the question
        # THEN a typeerror is thrown
        with pytest.raises(TypeError):
            question_list.add_group(True)

    def test_add_groups(self, question_list: QuestionList,
            open_question_group: QuestionGroup,
            likert_question_group: QuestionGroup):
        # GIVEN a question list and two question groups
        # WHEN we add the question groups at once
        # THEN all the question groups are added
        question_list.add_groups([open_question_group, likert_question_group])
        group_ids = [g.id for g in question_list.groups.all()]
        assert open_question_group.id in group_ids
        assert likert_question_group.id in group_ids
