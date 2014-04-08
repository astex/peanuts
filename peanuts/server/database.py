from flask.ext.sqlalchemy import SQLAlchemy

def register( app ):
    db = SQLAlchemy(app)
    db.app = app
    from peanuts.models import *
    db.create_all()
