"""Models for manipulating an application."""


import os
from enum import IntEnum
from datetime import datetime

from peanuts.lib.database import db
from peanuts.models.base import Model


__all__ = ['Application']


class Application(Model):
    """An application.

        An application is a database representation of a frontend app.
    """
    __tablename__ = 'application'

    class Verbosity(IntEnum):
        none = 0
        admin = 1

    id_ = db.Column('id', db.Integer, primary_key=True)

    # A uuid that apps must send in to use the backend.  This is not meant to
    #   be a security feature, just a way of identifying which app the user is
    #   using.  It is exposed freely to the user and can be spoofed.
    token = db.Column(
        'token',
        db.Unicode,
        index=True,
        nullable=False
        )

    created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
        )

    title = db.Column(db.Unicode(255))
    description = db.Column(db.Unicode(255))
    slug = db.Column(db.Unicode(255)) # Relative url.
    repo_url = db.Column(db.Unicode(255))

    # A json dump of all configuration parameters for the app.
    config = db.Column(db.UnicodeText)

    def get_dictionary(self, verbosity='none'):
        """Return a serializable dictionary representation of the application.
        """
        verbosity = getattr(self.Verbosity, verbosity, -1)

        d = {
            'title': self.title,
            'config': self.config
            }

        if verbosity <= self.Verbosity.none:
            return d

        d.update({
            'created': self.created,
            'description': self.description,
            'url': self.url,
            'repo_url': self.repo_url
            })

        return d

    @property
    def static_dir(self):
        """Returns the relative location from which to server static files."""
        return os.path.join('front', self.slug, 'static')
