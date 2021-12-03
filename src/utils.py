import logging
from flask import has_request_context, request, redirect, url_for, Response
from typing import Union

from src.models import Case


class RequestFormatter(logging.Formatter):
    """A custom Formatter for logging."""

    def format(self, record):
        record.url = None
        record.remote_addr = None
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        return super().format(record)


def check_case() -> Union[Case, Response]:
    """Checks if the request has a 'sessionID' cookie and if this ID is
    linked to an existing case. If this is true, then the case is
    returned. If not, the user is redirected to the start page.
    """
    session_id = request.cookies.get("sessionID")
    if not session_id:
        return redirect(url_for("questions.start"))
    case = Case.query().filter_by(id=session_id).first()
    if not case:
        return redirect(url_for("questions.start"))
    return case