from flask import render_template, redirect, url_for

from src.blueprints.main import bp


@bp.route('/')
def index():
    return redirect(url_for("questions.start"))
    return render_template('index.html')
