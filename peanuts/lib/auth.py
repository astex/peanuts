"""A library for dealing with authentication."""


from functools import wraps
from copy import copy

from werkzeug.exceptions import Unauthorized


__all__ = [
    'Need', 'needs', 'no_need', 'login_need', 'no_login_need', 'admin_need'
    ]


class Need(object):
    """An authentication requirement.

        This can be used in a few different ways.  Calling the need returns a
        boolean which indicates whether or not the need is met.  This allows
        you to do things like this:

            ```
            if login_need():
                # Do stuff that requires a login.
            else:
                # Do other stuff that doesn't require a login.
            ```

        You can also use a need as a context, which will raise an Unauthorized
        exception if the need is not met:

            ```
            with login_need:
                # Do stuff that requires a login.
            ```

        Implementing a need is simple, just overwrite the is_met() method.

        While these will tend to be singletons (e.g login_need, admin_need,
        ...), they don't have to be.  One use case would be for owner
        permissions, which will likely require an argument when initializing
        the need.  For example:

            ```
            class ObjectOwnerNeed(Need):
                def is_met(self):
                    return bool(obj.owner == self.session.user)

            # later...
            owner_need = ObjectOwnerNeed(some_obj)
            with owner_need:
                # Do something only the owner of that object should do.
            ```
    """
    def __call__(self):
        return self.is_met()

    def __enter__(self):
        if not self():
            raise Unauthorized

    def __exit__(self, type_, value, traceback):
        pass

    @property
    def session(self):
        """The flask session."""
        from flask import session
        return session

    def is_met(self):
        """This should be overwritten for each need class.

            Returns:
                (bool) - True if the need is met, False otherwise.
        """
        return True

def needs(need):
    """A decorator to handle different needs.

        This wraps a function in a Need context so that an error is raised if
        the need is not met:

            ```
            @needs(login_need)
            def a_route(*args, **kargs):
                # Do some stuff that requires a login.
            ```
    """
    def adapt(f):
        @wraps(f)
        def decorated(*args, **kargs):
            with need:
                return f(*args, **kargs)
        return decorated
    return adapt

class NoNeed(Need):
    """The NoNeed is always met."""
    pass

class LoginNeed(Need):
    """A need that checks basic authentication."""
    def is_met(self):
        """Checks if the user is logged in."""
        return bool(self.session.user)

class NoLoginNeed(Need):
    """A need that checks that no user is logged in."""
    def is_met(self):
        """Checks that no user is logged in."""
        return not self.session.user

class AdminNeed(Need):
    """A need that checks if the user is an admin."""
    def is_met(self):
        """Checks if the user is an admin."""
        return bool(self.session.user and self.session.user.is_admin)

no_need = NoNeed()
login_need = LoginNeed()
no_login_need = NoLoginNeed()
admin_need = AdminNeed()
