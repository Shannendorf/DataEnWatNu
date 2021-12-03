import os
import logging
from flask import Flask
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask.wrappers import Request

from src import models
from src.blueprints import main, questions
from src.errors import bp as errors_bp
from src.extensions import bootstrap, db, migrate
from src.utils import RequestFormatter
from src.blueprints.questions.email import mail


def create_app(config_object: str = 'src.settings') -> Flask:
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config_object)
    app.jinja_env.globals.update(getattr=getattr)
    app.jinja_env.globals.update(list=list)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)


def register_blueprints(app):
    app.register_blueprint(errors_bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(questions.bp)


def register_shellcontext(app):
    def shell_context():
        return {
            'db': db,
            "QuestionType": models.QuestionType,
            "Question": models.Question,
            "Answer": models.Answer,
            "QuestionGroup": models.QuestionGroup,
            "Case": models.Case,
            "Code": models.Code,
            "QuestionList": models.QuestionList
        }
    app.shell_context_processor(shell_context)
