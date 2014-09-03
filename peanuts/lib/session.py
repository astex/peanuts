"""A library for dealing with session-based authentication."""


from flask import json
from flask.sessions import SessionMixin, SessionInterface


__all__ = ['PeanutsSessionInterface']


class PeanutsSession(dict, SessionMixin):
    """A custom session object for use with peanuts."""
    @property
    def user(self):
        """The user, taken from the database, if it exists."""
        from peanuts.lib.database import db
        from peanuts.models.user import User
        return db.session.query(User).get(self.get('user_id'))

    @property
    def public_dict(self):
        """The dictionary to actually display."""
        return self.get('user_id')

    @property
    def serialized(self):
        """Cookies can't store dicts..."""
        return json.dumps(dict(self))

class PeanutsSessionInterface(SessionInterface):
    """A custom session interface for use with peanuts."""
    def open_session(self, app, request):
        """Loads the session from the request."""
        # C is for cookie.
        c = request.cookies.get(app.session_cookie_name)
        if not c:
            # No cookie, provide no session.
            return PeanutsSession()
        else:
            return PeanutsSession(c)

    def save_session(self, app, session, response):
        """Saves the session to the response."""
        domain = self.get_cookie_domain(app)
        if not session:
            if session.modified:
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain
                    )
            return

        response.set_cookie(
            app.session_cookie_name,
            session.serialized,
            expires=self.get_expiration_time(app, session),
            httponly=True,
            domain=domain
            )
