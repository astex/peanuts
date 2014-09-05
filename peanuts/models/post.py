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

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # This post is a reply to its parent.
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', ondelete='CASCADE')
        )

    # This post is in the same thread as the root.
    root_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    content = db.Column(db.UnicodeText, nullable=False)
    state = db.Column(db.Enum('draft', 'posted', 'deleted'), default='draft')

    owner = db.relationship('User')

    parent = db.relationship(
        'Post',
        primaryjoin='Post.parent_id == Post.id_',
        foreign_keys='Post.parent_id',
        remote_side='Post.id_'
        )
    root = db.relationship(
        'Post',
        primaryjoin='Post.root_id == Post.id_',
        foreign_keys='Post.root_id',
        remote_side='Post.id_'
        )
