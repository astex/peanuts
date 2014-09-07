"""Views and routing."""


import os

from werkzeug.exceptions import NotFound
from flask import render_template, send_from_directory

from peanuts.views import post, user, session
from peanuts.lib.database import db
from peanuts.models.app import Application


def register(app, route_base=''):
    """Registers views with the app."""
    post.PostView.register(app, route_base=route_base + '/post/')
    user.UserView.register(app, route_base=route_base + '/user/')
    session.SessionView.register(app, route_base=route_base + '/session/')
    session.AuthPeanutsView.register(
        app,
        route_base=route_base + '/session/peanuts/'
        )

    @app.route('/<string:app_name>/')
    def app_index(app_name):
        """Registers all in-house frontend applications."""
        application = db.session.query(Application).filter(
            Application.slug == app_name
            ).first()
        if not application:
            raise NotFound

        return render_template('index.html', frontend=application)

    @app.route('/<string:app_name>/<path:file_name>')
    def app_static(app_name, file_name):
        """Provides static files for the given frontend application."""
        application = db.session.query(Application).filter(
            Application.slug == app_name
            ).first()

        if not application:
            raise NotFound

        return send_from_directory(
            os.path.join(app.root_path, application.static_dir),
            file_name
            )
