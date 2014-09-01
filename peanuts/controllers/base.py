"""Base controller(s) which take in a dictionary and return a model."""


from peanuts.database import db


__all__ = ['BaseRestController']


class BaseRestController(object):
    """A base class for RESTful controllers."""
    Model = None

    def index(self, get_data):
        """Returns a list of models based on filters in get_data."""
        return db.session.query(self.Model).all()
