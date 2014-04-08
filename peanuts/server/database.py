from flask.ext.sqlalchemy import SQLAlchemy

def register( app ):
    db = SQLAlchemy()
    db.app = app
    from peanuts.models import *
    db.create_all()
