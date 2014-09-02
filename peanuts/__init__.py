"""The peanuts backend application."""


from flask import Flask


__all__ = ['create_app']


def create_app(config):
    """Creates a default application."""
    app = Flask(__name__)
    app.config.from_pyfile(config)

    from peanuts.lib.database import db
    db.init_app(app)

    from peanuts import views
    views.register(app)

    with app.app_context():
        db.create_all()

    return app
