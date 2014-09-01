"""Base controller(s) which take in a dictionary and return a model."""


from peanuts.database import db


__all__ = ['BaseRestController']


class BaseRestController(object):
    """A base class for RESTful controllers."""
    Model = None

    def index(self, filter_data=None):
        """Returns a list of models based on filters in filter_data."""
        if filter_data is None:
            filter_data = {}

        return db.session.query(self.Model).all()

    def get(self, id_, filter_data=None):
        """Retuns a single object based on filters in filter_data."""
        if filter_data is None:
            filter_data = {}

        return db.session.query(self.Model).get(id_)

    def post(self, post_data, filter_data=None):
        """Posts a new object and returns it."""
        if filter_data is None:
            filter_data = {}

        model = self.Model(**post_data)
        db.session.add(model)
        db.session.commit()

        return model
