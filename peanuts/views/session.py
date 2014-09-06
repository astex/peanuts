"""View(s) for dealing with authentication and the session object."""


from needs import needs

from flask.ext.classy import route

from peanuts.lib.auth import login_need
from peanuts.views.base import BaseView
from peanuts.controllers.session import (
    SessionController, AuthPeanutsController
    )

__all__ = ['SessionView']


class SessionView(BaseView):
    """The view for generic session operations."""
    Controller = SessionController

    @route('/', methods=['GET'])
    @needs(login_need)
    def get(self):
        """Returns the current session object."""
        return self.jsonify(self.controller.get())

    @route('/', methods=['DELETE'])
    @needs(login_need)
    def delete(self):
        """Deletes the current session (logs out a user)."""
        return self.jsonify(self.controller.delete())

class AuthPeanutsView(BaseView):
    """The view for authenticating a peanuts session."""
    Controller = AuthPeanutsController

    def post(self):
        """Posts a new session via auth peanuts (logs in)."""
        return self.jsonify(self.controller.post(self.data))
