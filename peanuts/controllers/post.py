"""Controller(s) for manipulating posts."""


from peanuts.models.post import Post
from peanuts.controllers.base import BaseRestController


__all__ = ['PostController']


class PostController(BaseRestController):
    """A controller for manipulating posts."""
    Model = Post
