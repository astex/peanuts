"""Models for manipulating a post."""


from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

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
    state = db.Column(db.Enum('draft', 'posted', 'deleted'), default='draft')

class PostSubModel(Model):
    """An abstract base for Post submodels."""
    __abstract__ = True

    @declared_attr
    def post(cls):
        """The relationship to the post."""
        return db.relationship('Post', backref='data')

class Reply(Model):
    """A more detailed view of a posting with additional information relevant
        to replies.
    """
    __tablename__ = 'reply'

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    parent_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship(
        'Post',
        backref='reply_data',
        primaryjoin='Reply.post_id == Post.id_'
        )
    parent_post = db.relationship(
        'Post',
        backref='replies',
        primaryjoin='Reply.parent_post_id == Post.id_'
        )
