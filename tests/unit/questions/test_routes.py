from typing import List
from flask.testing import FlaskClient
from pytest_mock.plugin import MockerFixture

from src.models import Answer, Case, Code, QuestionGroup, QuestionList, Question

from tests.helpers.request_helpers import send_get, send_post


class TestStartRoute:
    URL = "/questions/start"

    def test_start_route(self, client: FlaskClient):
        """Test the question start route."""
        # GIVEN a client
        # WHEN the user visits the start route
        # THEN the start page is shown
        resp = send_get(client, self.URL)
        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Start vragenlijst" in page

    def test_post_code(self, client: FlaskClient, code: Code):
        """Test posting a code to the start route."""
        # GIVEN a client and a code
        # WHEN the user posts a code
        # THEN a case is created and the user is redirected to the intro page
        resp = send_post(client, self.URL, data={"code": code.code})
        assert "Intro" in resp.data.decode()
        assert Case.query().count() == 1

    def test_post_wrong_code(self, client: FlaskClient):
        """Test posting a non-existing code to the start route."""
        # GIVEN a client and a non-existing code
        # WHEN the user posts the non-existing code
        # THEN an error message is shown
        resp = send_post(client, self.URL, data={"code": "NOSUCHCODE"})
        page = resp.data.decode()
        assert "Start vragenlijst" in page
        assert "Code onjuist" in page
        assert Case.query().count() == 0

    
class TestIntroRoute:
    URL = "/questions/intro"

    def test_intro_page(self, client: FlaskClient, question_list: QuestionList,
            case: Case):
        # GIVEN a client, a question list, and a case
        # WHEN we visit the intro page
        # THEN the intro page is shown
        client.set_cookie("localhost", "sessionID", case.id)
        resp = send_get(client, self.URL)
        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Intro" in page
        assert "Bedrijfsnaam" in page
        assert "Email" in page
        assert "Bedrijfsbranch" in page
        assert "Bedrijfsgrootte" in page
        assert "Uw functie" in page
        assert "Start vragenlijst" in page

    def test_post_data(self, client: FlaskClient, question_list: QuestionList,
            case: Case, open_question_group: QuestionGroup):
        # GIVEN a client, a question list, and a case
        # WHEN we post data to the intro page
        # THEN the user is redirected to the first question page
        question_list.add_group(open_question_group)
        data = {"company": "TComp", "email": "test@tcomp.com",
            "branch": "Productie", "company_size": "15",
            "participant_function": "Test"}
        client.set_cookie("localhost", "sessionID", case.id)
        resp = send_post(client, self.URL, data=data)
        assert resp.status_code == 200
        assert open_question_group.title in resp.data.decode()
        assert case.email == "test@tcomp.com"

    def test_no_case(self, client: FlaskClient, question_list: QuestionList):
        # GIVEN a client and a question list
        # WHEN the user visits the intro page
        # THEN the user is redirected to the start page
        resp = send_get(client, self.URL)
        assert resp.status_code == 302

    def test_multiple_lists(self, client: FlaskClient, case: Case,
            question_lists: List[QuestionList]):
        # GIVEN a client, a case, and a number of question lists
        # WHEN the user visits the intro page
        # THEN the intro page is shown with a list selector
        client.set_cookie("localhost", "sessionID", case.id)
        resp = send_get(client, self.URL)
        page = resp.data.decode()
        for question_list in question_lists:
            question_list.name in page    
            
    def test_post_data_multiple_lists(self, client: FlaskClient, case: Case,
            question_lists: List[QuestionList],
            open_question_group: QuestionGroup):
        # GIVEN a client, a number of question lists, and a case
        # WHEN we post data to the intro page
        # THEN the user is redirected to the first question page
        question_lists[1].add_group(open_question_group)
        data = {"company": "TComp", "email": "test@tcomp.com",
            "branch": "Productie", "company_size": "15",
            "participant_function": "Test",
            "selection": str(question_lists[1].id)}
        client.set_cookie("localhost", "sessionID", case.id)
        resp = send_post(client, self.URL, data=data)
        assert resp.status_code == 200
        assert open_question_group.title in resp.data.decode()
        assert case.email == "test@tcomp.com"


class TestQuestionRoute:
    URL = "/questionlist/{q_id}"

    def test_question_page(self, client: FlaskClient, case: Case,
            question_list: QuestionList, open_question_group: QuestionGroup):
        # GIVEN a client, a case, and a question list with questions
        # WHEN the user visits the page for a question
        # THEN the question page is opened for the correct question
        question_list.add_group(open_question_group)
        case.update(case_list=question_list)
        client.set_cookie("localhost", "sessionID", case.id)
        resp = send_get(client, self.URL.format(q_id=0))
        assert resp.status_code == 200
        page = resp.data.decode()
        assert open_question_group.title in page
        for question in open_question_group.questions.all():
            assert question.question in page

    def test_question_page_last_question(self, client: FlaskClient, case: Case,
            question_list: QuestionList, open_question_group: QuestionGroup):
        # GIVEN a client, a case, and a question list with questions
        # WHEN the user visits the page for a question id out of the range
        # THEN the user is redirected to the advice page
        question_list.add_group(open_question_group)
        case.update(case_list=question_list)
        client.set_cookie("localhost", "sessionID", case.id)
        resp = send_get(client, self.URL.format(q_id=42))
        assert resp.status_code == 302

    def test_post_data(self, client: FlaskClient, case: Case,
            mocker: MockerFixture, question_list: QuestionList,
            open_question_group: QuestionGroup, open_question: Question):
        # GIVEN a client, a case, and a question list with questions
        # WHEN the user posts the answersr to a question
        # THEN the answer is posted
        patch_base = "src.blueprints.questions.routes"
        mocker.patch(f"{patch_base}.generate_report", return_value="REPORT")
        mocker.patch(f"{patch_base}.generate_radarchart",
            return_value="REPORT")
        question_list.add_group(open_question_group)
        case.update(case_list=question_list)
        client.set_cookie("localhost", "sessionID", case.id)
        data = {"q0": "TEST"}
        resp = send_post(client, self.URL.format(q_id=0), data=data)
        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Overzicht Resultaten" in page
        answer = Answer.query().first()
        assert answer.answer == "TEST"

    def test_post_reanswer_question(self, client: FlaskClient, case: Case,
            mocker: MockerFixture, question_list: QuestionList,
            open_question_group: QuestionGroup, open_question: Question,
            open_answer: Answer):
        # GIVEN a client, a case, and a question list with questions that
        #   already have an answer
        # WHEN the user posts the answers to a question already answered
        # THEN the original answer is overwritten
        patch_base = "src.blueprints.questions.routes"
        mocker.patch(f"{patch_base}.generate_report", return_value="REPORT")
        mocker.patch(f"{patch_base}.generate_radarchart",
            return_value="REPORT")
        question_list.add_group(open_question_group)
        case.update(case_list=question_list)
        client.set_cookie("localhost", "sessionID", case.id)
        old_answer = open_answer.answer
        data = {"q0": "NEW ANSWER"}
        resp = send_post(client, self.URL.format(q_id=0), data=data)
        assert resp.status_code == 200
        page = resp.data.decode()
        assert "Overzicht Resultaten" in page
        answer = Answer.query().first()
        assert answer.answer != old_answer
        assert answer.answer == "NEW ANSWER"

        