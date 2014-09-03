"""Models for dealing with users and different authentication providers."""

import bcrypt
from datetime import datetime

from peanuts.lib.database import db
from peanuts.models.base import Model


__all__ = ['User', 'UserData', 'PeanutsAuth']


class User(Model):
    """The base user model on which to tie in information and auth providers.
    """
    __tablename__ = 'user'

    id_ = db.Column('id', db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
        )
    last_login = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
        )

class UserData(Model):
    """The personal data tied to a given user."""
    __tablename__ = 'user_data'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    email = db.Column(db.Unicode(255), index=True, unique=True)

    first_name = db.Column(db.UnicodeText)
    last_name = db.Column(db.UnicodeText)

class PeanutsAuth(Model):
    """A basic authentication provider for peanuts."""
    __tablename__ = 'peanuts_auth'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # This may or may not differ from UserData.email and should be used
    #   exclusively to authenticate a user.
    email = db.Column(db.Unicode(255), index=True, unique=True)

    # This should be a bcrypt hash.
    _password = db.Column('password', db.Unicode(60))

    @property
    def password(self):
        """Just returns _password.  Necessary to have a setter."""
        return self._password

    @password.setter
    def password(self, value):
        """Sets the password to a bcrypted hash."""
        self._password = bcrypt.hashpw(value, bcrypt.gensalt())

    def has_password(self, password):
        """Checks if the user has the provided password."""
        return bcrypt.hashpw(password, self.password) == self.password

    def get_dictionary(self, verbosity='none'):
        """Auth providers should generally not display any information directly
            to the frontend.
        """
        return False
