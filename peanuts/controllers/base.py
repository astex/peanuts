"""Base controller(s) which take in a dictionary and return a model."""

from flask import request

from peanuts.lib.database import db


__all__ = ['BaseRestController']


class BaseController(object):
    """A base controller class with some utility functions."""
    def __init__(self):
        self.request = request
        self.db_session = db.session

    def commit(self):
        """A wrapper for database commits which rolls them back if they fail.
        """
        try:
            self.db_session.commit()
        except:
            self.db_session.rollback()

class BaseRestController(BaseController):
    """A base class for RESTful controllers."""
    Model = None

    def index(self, filter_data=None):
        """Returns a list of models based on filters in filter_data."""
        if filter_data is None:
            filter_data = {}

        return self.db_session.query(self.Model).all()

    def get(self, id_):
        """Retuns a single object based on filters in filter_data."""
        return self.db_session.query(self.Model).get(id_)

    def post(self, post_data):
        """Posts a new object and returns it."""
        model = self.Model(**post_data)
        self.db_session.add(model)
        self.commit()

        return model

    def put(self, id_, post_data):
        """Updates an existing object with new data."""
        model = self.db_session.query(self.Model).get(id_)
        for key in post_data:
            setattr(model, key, post_data[key])
        self.db_session.add(model)
        self.commit()

        return model

    def delete(self, id_):
        """Deletes an existing object."""
        model = self.db_session.query(self.Model).get(id_)
        self.db_session.delete(model)
        self.commit()
