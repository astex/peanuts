"""The peanuts backend application.

    copyright 2014 Phil Condreay (0astex@gmail.com)

    Peanuts is released under the MIT license.  If a copy of the license was
    not distributed with this code, see http://opensource.org/licenses/MIT.
"""


from werkzeug.exceptions import default_exceptions
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

    from peanuts.lib.session import PeanutsSessionInterface
    app.session_interface = PeanutsSessionInterface()

    from peanuts.lib.err import make_json_error
    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_json_error

    return app
