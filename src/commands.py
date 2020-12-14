from flask.cli import FlaskGroup
from secrets import token_urlsafe

from src.app import create_app
from src.database import db

cli = FlaskGroup(create_app=create_app)
app = create_app()


@cli.command()
def drop_db():
    db.drop_all()
    db.session.commit()
