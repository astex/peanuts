"""The peanuts backend application.

    copyright 2014 Phil Condreay (0astex@gmail.com)

    Peanuts is released under the MIT license.  If a copy of the license was
    not distributed with this code, see http://opensource.org/licenses/MIT.
"""


import json, uuid

from werkzeug.exceptions import default_exceptions, NotFound
from flask import Flask


__all__ = ['create_app']


def create_app(config):
    """Creates a default application."""
    app = Flask(__name__)
    app.config.from_pyfile(config)

    from peanuts.lib.database import db
    db.init_app(app)

    from peanuts import views
    views.register(app, route_base='/api')

    with app.app_context():
        from peanuts.models.app import Application
        from peanuts.lib.auth import no_apps_need

        db.create_all()

        @app.before_first_request
        def check_admin(*args, **kargs):
            """Checks that there is an admin application.  If not, creates it.
            """
            if no_apps_need():
                # Unless overridden by a direct database operation, the first
                #   app to be accessed should be admin.
                admin_app = Application(
                    token='6752e4b0-8122-4c9a-ad1d-19d703fdfed0',
                    title='Admin',
                    description='The administrative application.',
                    slug='admin',
                    repo_url=app.config['ADMIN_REPO'],
                    config=json.dumps('{}')
                    )
                db.session.add(admin_app)
                db.session.commit()

    from peanuts.lib.session import PeanutsSessionInterface
    app.session_interface = PeanutsSessionInterface()

    from peanuts.lib.err import make_json_error
    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_json_error

    return app
