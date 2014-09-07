"""A library for dealing with session-based authentication."""


from flask.sessions import SecureCookieSession, SecureCookieSessionInterface


__all__ = ['PeanutsSessionInterface']


class PeanutsSession(SecureCookieSession):
    """A custom session object for use with peanuts."""
    def __init__(self, *args, **kargs):
        """Initializes this with an application uuid taken from the request
            headers.
        """
        super(PeanutsSession, self).__init__(*args, **kargs)

        from flask import request
        self.application_id = request.headers.get('X-PEANUTS-APPLICATION')

    @property
    def application(self):
        """The application, taken from the database, if it exists."""
        from peanuts.lib.database import db
        from peanuts.models.app import Application
        if self.application_id:
            return db.session.query(Application).get(application_id)
        else:
            return None

    @property
    def user(self):
        """The user, taken from the database, if it exists."""
        from peanuts.lib.database import db
        from peanuts.models.user import User
        user_id = self.get('user_id')
        if user_id:
            return db.session.query(User).get(user_id)
        else:
            return None

    @property
    def public_dict(self):
        """The dictionary to actually display."""
        return {'user_id': self.get('user_id')}

class PeanutsSessionInterface(SecureCookieSessionInterface):
    """A custom session interface for use with peanuts."""
    session_class = PeanutsSession
