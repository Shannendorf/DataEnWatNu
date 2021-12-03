from flask import request
from flask.testing import FlaskClient

from src.errors import _wants_json_response, _html_error_response, \
    _api_error_response, error_response 


class TestWantsJsonResponse:

    def tests_want_json_response(self, app: FlaskClient):
        # GIVEN an application context
        # WHEN we check if it wants a json response
        # THEN True is returned
        with app.test_request_context():
            assert _wants_json_response()


class TestHtmlErrorResponse:

    def test_html_error_response(self, app: FlaskClient):
        # GIVEN an application context
        # WHEN we request an HTML error response
        # THEN a HTML error page and status code are returned
        with app.test_request_context():
            page, status = _html_error_response(404, "Not found", "not found")
        assert "404" in page
        assert "Not found" in page
        assert "not found" in page
        assert status == 404


class TestApiErrorResponse:

    def test_api_error_response(self, app: FlaskClient):
        # GIVEN an application context
        # WHEN we request a JSON error response
        # THEN a JSON error response is returned
        with app.test_request_context():
            resp = _api_error_response(404, "Not found", "not found")
        assert resp.is_json
        data = resp.get_json()
        assert data == {
            "status-code": 404,
            "error": "Not found",
            "message": "not found"
        }
        assert resp.status_code == 404


class TestErrorResponse:
    class TestStatus:
        code = 404

    def test_error_response(self, app: FlaskClient):
        # GIVEN an application context
        # WHEN we request an error response
        # THEN a error response is returned
        with app.test_request_context():
            resp = error_response(self.TestStatus(), "Test")
        assert resp.is_json
        assert resp.status_code == 404 
