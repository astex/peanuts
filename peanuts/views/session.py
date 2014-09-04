"""View(s) for dealing with authentication and the session object."""


from flask.ext.classy import route

from peanuts.lib.auth import needs, login_need
from peanuts.views.base import BaseView
from peanuts.controllers.session import SessionController


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
