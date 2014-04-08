from flask import Flask

from .server import database, auth

from .lib.exception import BaseError, ServerError

def create_app(config='config', app_name=__name__):
    """Flask application factory."""

    class PeanutsFlask(Flask):
        """App subclass to implement any methods overriding the default."""

        def handle_user_exception(self, e):
            """Overrides the default exception handler so that responses can be a little more dynamic.
            
                Note that this deliberately breaks default error handling.  All manually-raised exceptions
                should inherit from lib.exceptions.BaseError.
            """

            if issubclass(e, BaseError) or isinstance(e, BaseError):
                return e.response

            if self.debug:
                raise e
            else:
                return ServerError.from_exception(e).response

    app = PeanutsFlask( app_name )

    database.register(app)
    auth.register(app)

    from . import views
    views.register(app)

    return app
