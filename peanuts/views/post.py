"""View(s) for manipulating posts."""


from peanuts.views.base import BaseRestView
from peanuts.controllers.post import PostController


__all__ = ['PostView']


class PostView(BaseRestView):
    """A view for manipulating posts."""
    Controller = PostController
