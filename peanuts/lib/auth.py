"""A library for dealing with authentication."""


from needs import Need

from werkzeug.exceptions import Unauthorized


__all__ = 'SelfNeed', 'no_apps_need', 'app_need', 'login_need', 'admin_need'


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

class ApplicationNeed(FlaskNeed):
    """A need that checks for a valid application."""
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
    def is_met(self):
        """Checks if the user is logged in."""
        return bool(self.session.user)

class AdminNeed(FlaskNeed):
    """A need that checks if the user is an admin."""
    def is_met(self):
        """Checks if the user is an admin."""
        return bool(self.session.user and self.session.user.is_admin)

class NoUserNeed(FlaskNeed):
    """A need that checks that there are no registered users."""
    def is_met(self):
        from peanuts.models.user import User

        return not self.db_session.query(
            self.db_session.query(User).exists()
            ).first()[0]

class SelfNeed(FlaskNeed):
    """Checks that the user is looking at itself."""
    def __init__(self, user_id):
        self.user_id = user_id

    def is_met(self):
        """Checks if the user_id is the user_id in the session."""
        return bool(
            (
                self.session.user and
                str(self.session.user.id) == self.user_id
                ) or
            admin_need()
            )

no_apps_need = NoApplicationsNeed()
app_need = ApplicationNeed()
login_need = LoginNeed()
admin_need = AdminNeed()
no_user_need = NoUserNeed()
