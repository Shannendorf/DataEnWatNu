import pytest
import subprocess
import os
from flask.app import Flask
from flask.testing import FlaskClient

from src.app import create_app
from src.extensions import db
from tests._fixtures import *

basedir = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".."))


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY="TESTING"
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app() -> Flask:
    test_config = TestConfig()
    app = create_app(test_config)
    
    ctx = app.app_context()
    ctx.push()

    db.create_all()
    db.session.commit()
    app.test_db = db

    yield app

    db.drop_all()
    ctx.pop()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
