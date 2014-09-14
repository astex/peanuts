"""View(s) for manipulating users."""


from needs import no_need

from peanuts.lib.auth import (
    SelfNeed, login_need, admin_need, no_admin_need
    )
from peanuts.models.user import User
from peanuts.views.base import BaseRestView
from peanuts.controllers.user import UserController


__all__ = ['UserView']


class UserView(BaseRestView):
    """A view for manipulating users."""
    Controller = UserController

    def index(self):
        """Checks that the verbosity is at an acceptable level based on the
            session before allowing the index.
        """
        verbosity = getattr(User.Verbosity, self.verbosity, -1)
        need = no_need

        if verbosity >= User.Verbosity.self:
            need = admin_need
        elif verbosity >= User.Verbosity.other:
            need = login_need

        with need:
            return super(UserView, self).index()

    def get(self, id_):
        """Checks that the verbosity is at an acceptable level based on the
            session before allowing the get.
        """
        verbosity = getattr(User.Verbosity, self.verbosity, -1)
        need = no_need

        if verbosity >= User.Verbosity.admin:
            need = admin_need
        elif verbosity >= User.Verbosity.self:
            need = SelfNeed(id_)
        elif verbosity >= User.Verbosity.other:
            need = login_need

        with need:
            return super(UserView, self).get(id_)

    def post(self):
        """Checks that the current user is allowed to post this kind of user
            before allowing the posting.
        """
        verbosity = getattr(User.Verbosity, self.verbosity, -1)

        # Non-logged-in or admin users may freely create new users.
        need = admin_need | ~login_need

        # We should be able to create a first admin account regardless of the
        #   situation.  After that, only an admin may create other admin
        #   accounts.
        if self.data.get('is_admin'):
            need = admin_need | no_admin_need
        elif verbosity >= User.Verbosity.admin:
            need = admin_need

        # There's no need to check SelfNeed or lower since this will log in the
        #   new user if successful.

        with need:
            return super(UserView, self).post()

    def put(self, id_):
        """Checks that the session has permission to edit the user before
            allowing the put.
        """
        verbosity = getattr(User.Verbosity, self.verbosity, -1)
        need = SelfNeed(id_)

        if verbosity >= User.Verbosity.admin:
            need = admin_need

        with need:
            return super(UserView, self).put(id_)

    def delete(self, id_):
        """Checks that the session has permission to edit the user before
            allowing the delete.
        """
        # NOTE Verbosity doesn't matter here since nothing is returned.
        with SelfNeed(id_):
            return super(UserView, self).delete(id_)
