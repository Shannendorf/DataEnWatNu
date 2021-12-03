from flask import Flask
from logging import LogRecord, ERROR
from werkzeug.http import dump_cookie
from werkzeug.wrappers.response import Response

from src.models import Case
from src.utils import check_case, RequestFormatter


class TestRequestFormatter:
    """Tests for the request formatter."""
    rf = RequestFormatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] - [from %(remote_addr)s to %(url)s]')
    record = LogRecord(
        name="tests.test",
        level=ERROR,
        pathname="TEST",
        lineno=42,
        msg="TEST",
        func="test_request_formatter",
        args=tuple(),
        exc_info=None
    )

    def test_request_formatter(self, app):
        """Test the logging request formatter outside request context."""
        # WHEN we format a log record
        # THEN a correctly formatted log line is returned
        result = self.rf.format(self.record)
        expected = "ERROR: TEST [in TEST:42] - [from None to None]"
        assert expected in result

    def test_with_request_context(self, app):
        """Test the logging request formatter with request context."""
        # GIVEN an request context
        # WHEN we format a log record
        # THEN a correctly formatted log line is returned
        with app.test_request_context():
            result = self.rf.format(self.record)
        expected = "ERROR: TEST [in TEST:42] - [from None to http://localhost/]"
        assert expected in result


class TestCheckCase:
    """Tests for the check case utility."""

    def test_check_case(self, app: Flask, case: Case):
        """Test the check_case utility."""
        # GIVEN an app context and a case
        # WHEN the check_case utility is used
        # THEN the case is returned
        cookie = dump_cookie("sessionID", case.id)
        with app.test_request_context(environ_base={"HTTP_COOKIE": cookie}):
            actual = check_case()
        assert actual.id == case.id

    def test_no_session_id(self, app: Flask):
        """Test the check_case utility when no sessionID is available."""
        # GIVEN an app context
        # WHEN the check_case utility is used, but without sessionID
        # THEN the user is redirected to the start
        with app.test_request_context():
            actual = check_case()
        assert isinstance(actual, Response)
        assert actual.status == "302 FOUND"

    def test_wrong_id(self, app: Flask):
        """Test the check_case utility when a sessionID is found, but does
        not match to any case.
        """
        # GIVEN an app context and a sessionID that is not linked to any case
        # WHEN the check_case utility is used
        # THEN the user is redirected to the start
        cookie = dump_cookie("sessionID", "DOESNOTEXIST")
        with app.test_request_context(environ_base={"HTTP_COOKIE": cookie}):
            actual = check_case()
        assert isinstance(actual, Response)
        assert actual.status == "302 FOUND"
