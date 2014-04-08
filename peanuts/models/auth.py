from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from peanuts import db
from peanuts.lib.password import Password

from .base import Model

class User(Model):
    """A user.
    
        This is the centralized user account to which everything should join.  Individual types of authentication
        should have their own associated model.
    """

    __tablename__ = 'user'

    id = db.Column( db.Integer(), primary_key=True )
    created = db.Column( db.DateTime(), nullable=False, default=func.now() )
    last_login = db.Column( db.DateTime(), nullable=False, default=func.now() )

    data = db.relationship('UserData', cascade='delete')

    auth_peanut = db.relationship('AuthPeanut')
    auth_admin = db.relationship('AuthAdmin')

    @property
    def roles(self):
        """The roles present for this user."""

        roles = set()

        if self.auth_peanut:
            roles.add('user')
        if self.auth_admin:
            roles.add('admin')
            roles.add('user')

        return roles

    dict_opts = {
        'include': ['roles']
    }

class UserData(Model):
    """Data belonging to a user."""

    __tablename__ = 'user_data'

    user_id = db.Column( db.Integer(), db.ForeignKey('user.id'), primary_key=True ),
    updated = db.Column( db.DateTime, nullable=False, default=func.now(), onupdate=func.now() )
    
    username = db.Column( db.Unicode(255), index=True )

    user = db.relationship('User')

class SimpleAuthMixin(object):
    """A simple email/password mixin."""

    user_id = db.Column( db.Integer(), db.ForeignKey('user.id'), primary_key=True )
    created = db.Column( db.DateTime, nullable=False, default=func.now() )
    updated = db.Column( db.DateTime, nullable=False, default=func.now(), onupdate=func.now() )

    email = db.Column( db.Unicode(255), nullable=False, index=True, unique=True )
    _password = db.Column( 'password', db.Unicode(255), nullable=False )

    @property
    def password(self): return Password(self._password)
    @password.setter
    def password(self, pw): self._password = Password.hashpw(pw).hashed

    @declared_attr
    def user(cls): return db.relationship('User')

    dict_opts = {
        'exclude': ['_password']
    }

class AuthPeanut(Model, SimpleAuthMixin):
    """Simple cookie-based authentication via email/passord."""

    pass

class AuthAdmin(Model, SimpleAuthMixin):
    """Simple cookie-based admin authentication via email/password."""

    pass
