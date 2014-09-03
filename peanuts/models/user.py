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

    data = db.relationship('UserData', backref='user')
    peanuts_auth = db.relationship('PeanutsAuth', backref='user')

    def get_dictionary(self, verbosity='none'):
        """User dictionaries do and should vary based on the user accessing the
            information.  Here this is represented by verbosity, which is
            checked against the session user at the view level.
        """
        # The verbosity here is hierarchical by nature, so we enumerate it via
        #   the following dict.
        verbosity = {
            'none': 0,
            'other': 1,
            'self': 2,
            'admin': 3
            }.get(verbosity, -1)

        d = {}

        if verbosity <= 0:
            return d

        d.update({
            'user_name': self.data.user_name
            })

        if verbosity <= 1:
            return d

        d.update({
            'email': self.data.email,
            'first_name': self.data.first_name,
            'last_name': self.data.last_name,
            'created': self.created,
            'last_login': self.last_login
            })

        if verbosity <= 2:
            return d

        d.update({
            'has_peanuts_auth': bool(self.peanuts_auth)
            })

        return d

class UserData(Model):
    """The personal data tied to a given user."""
    __tablename__ = 'user_data'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        ondelete='CASCADE'
        )

    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
        )

    email = db.Column(db.Unicode(255), index=True, unique=True)

    first_name = db.Column(db.UnicodeText)
    last_name = db.Column(db.UnicodeText)

    # A public-facing display name to show on posts.
    user_name = db.Column(db.Unicode(255))

class PeanutsAuth(Model):
    """A basic authentication provider for peanuts."""
    __tablename__ = 'peanuts_auth'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        ondelete='CASCADE'
        )

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
