"""A library for dealing with session-based authentication."""


from werkzeug.exceptions import Forbidden
from flask.sessions import SecureCookieSession, SecureCookieSessionInterface


__all__ = ['PeanutsSessionInterface']


class PeanutsSession(SecureCookieSession):
    """A custom session object for use with peanuts."""
    @property
    def request(self):
        """Returns the flask request."""
        from flask import request
        return request

    @property
    def application(self):
        """The application, taken from the database, if it exists."""
        from flask import request
        from peanuts.lib.database import db
        from peanuts.models.app import Application

        application_id = request.headers.get('x-peanuts-application')
        if application_id:
            return db.session.query(Application).filter(
                Application.token == application_id
                ).first()
        else:
            return None

    @property
    def user(self):
        """The user, taken from the database, if it exists.

            The csrf token is checked here so that any and all endpoints
            requiring a user must have csrf protection.
        """
        from peanuts.lib.database import db
        from peanuts.models.user import User

        csrf = self.get('csrf')
        header_csrf = self.request.headers.get('x-peanuts-csrf')

        if (
                not csrf or
                csrf and not header_csrf or
                csrf != header_csrf
            ):
            raise Forbidden('CSRF token rejected.')

        user_id = self.get('user_id')
        if user_id:
            return db.session.query(User).get(user_id)
        else:
            return None

    @property
    def public_dict(self):
        """The dictionary to actually display."""
        return {'user_id': self.get('user_id')}

    def clear(self, *args, **kargs):
        """Let's the csrf persist across cleared sessions."""
        csrf = self.get('csrf')
        super(PeanutsSession, self).clear(*args, **kargs)
        self['csrf'] = csrf

class PeanutsSessionInterface(SecureCookieSessionInterface):
    """A custom session interface for use with peanuts."""
    session_class = PeanutsSession
