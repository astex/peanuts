"""Controller(s) for dealing with authentication and the session object."""


from peanuts.controllers.base import BaseController


__all__ = ['SessionController']


class SessionController(BaseController):
    """The controller for generic session operations."""
    def get(self):
        """Returns a public view of the session."""
        return self.session.public_dict

    def delete(self):
        """Clears the session (logs out)."""
        self.session.clear()
