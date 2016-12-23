from app import app
from db import db
from flask import session

db.init_app(app)


@app.before_first_request
def create_tables():
    session['username'] = None
    db.create_all()
