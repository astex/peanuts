"""Models for manipulating a post."""


from datetime import datetime

from peanuts.lib.database import db
from peanuts.models.base import Model


__all__ = ['Post']


class Post(Model):
    """A basic posting."""
    __tablename__ = 'post'

    id_ = db.Column('id', db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
        )
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
        )
    content = db.Column(db.UnicodeText, nullable=False)
