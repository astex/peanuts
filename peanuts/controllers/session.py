"""Controller(s) for dealing with authentication and the session object."""


from datetime import datetime

from werkzeug.exceptions import BadRequest

from peanuts.controllers.base import BaseController
from peanuts.models.user import PeanutsAuth


__all__ = ['SessionController']


class SessionController(BaseController):
    """The controller for generic session operations."""
    def get(self):
        """Returns a public view of the session."""
        return self.session.public_dict

    def delete(self):
        """Clears the session (logs out)."""
        self.session.clear()

class AuthPeanutsController(BaseController):
    """The controller for auth peanuts sessions."""
    def post(self, data):
        """Populates a peanuts session (logs in)."""
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise BadRequest('Email and password are required.')

        auth_peanuts = self.db_session.query(PeanutsAuth).filter(
            PeanutsAuth.email == email
            ).first()

        if not auth_peanuts:
            raise BadRequest('There is no peanuts user with that email.')

        if not auth_peanuts.has_password(password):
            raise BadRequest('That password is incorrect.')

        self.session.clear()
        self.session['user_id'] = auth_peanuts.user_id
        self.session.permanent = data.get('stay_logged_in')

        # Update last_login.
        self.session.user.last_login = datetime.utcnow()
        self.db_session.add(self.session.user)
        self.commit()

        return self.session.public_dict
