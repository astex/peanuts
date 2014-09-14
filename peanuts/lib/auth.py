"""A library for dealing with authentication."""


from needs import Need

from werkzeug.exceptions import Unauthorized, Forbidden


__all__ = [
    'SelfNeed', 'no_apps_need', 'app_need', 'login_need', 'admin_need',
    'csrf_need'
    ]


class FlaskNeed(Need):
    """A basic need with some handy flask wrapping."""
    error = Unauthorized

    @property
    def session(self):
        """The flask session."""
        from flask import session
        return session

    @property
    def db_session(self):
        """The database session."""
        from peanuts.lib.database import db
        return db.session

    @property
    def request(self):
        """The flask request."""
        from flask import request
        return request

class ApplicationNeed(FlaskNeed):
    """A need that checks for a valid application."""
    error = Forbidden('Please submit a valid app token.')

    def is_met(self):
        return bool(self.session.application)

class NoApplicationsNeed(FlaskNeed):
    """A need that checks that no applications exist."""
    def is_met(self):
        from peanuts.models.app import Application
        return not self.db_session.query(
            self.db_session.query(Application).exists()
            ).first()[0]

class LoginNeed(FlaskNeed):
    """A need that checks basic authentication."""
    error = Unauthorized('That requires a login.')

    def is_met(self):
        """Checks if the user is logged in."""
        return bool(self.session.user)

class AdminNeed(FlaskNeed):
    """A need that checks if the user is an admin."""
    error = Unauthorized('That requires admin credentials.')

    def is_met(self):
        """Checks if the user is an admin."""
        return bool(self.session.user and self.session.user.is_admin)

class NoAdminNeed(FlaskNeed):
    """A need that checks that there are no registered users."""
    error = Unauthorized('No admin users may be registered.')

    def is_met(self):
        from peanuts.models.user import User

        return not self.db_session.query(
            self.db_session.query(User).filter(User.is_admin == True).exists()
            ).first()[0]

class SelfNeed(FlaskNeed):
    """Checks that the user is looking at itself."""
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def error(self):
        """Raises an error which indicates the required user."""
        return Unauthorized(
            'Only the user with id {user_id} can do that.'.format(
                user_id=self.user_id
                )
            )

    def is_met(self):
        """Checks if the user_id is the user_id in the session."""
        return bool(
            (
                self.session.user and
                str(self.session.user.id) == self.user_id
                ) or
            admin_need()
            )

class CSRFNeed(FlaskNeed):
    """Checks that a valid csrf token is provided."""
    error = Forbidden(
        'A valid csrf token is required. Try refreshing the page.'
        )

    def is_met(self):
        """Checks the csrf token."""
        csrf = self.session.get('csrf')
        header_csrf = self.request.headers.get('x-peanuts-csrf')

        if (
                not csrf or
                csrf and not header_csrf or
                csrf != header_csrf
            ):
            return False
        return True

no_apps_need = NoApplicationsNeed()
app_need = ApplicationNeed()
login_need = LoginNeed()
admin_need = AdminNeed()
no_admin_need = NoAdminNeed()
csrf_need = CSRFNeed()
