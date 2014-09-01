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

    def get(self, id_):
        """Retuns a single object based on filters in filter_data."""
        return db.session.query(self.Model).get(id_)

    def post(self, post_data):
        """Posts a new object and returns it."""
        model = self.Model(**post_data)
        db.session.add(model)
        db.session.commit()

        return model

    def put(self, id_, post_data):
        """Updates an existing object with new data."""
        model = db.session.query(self.Model).get(id_)
        for key in post_data:
            setattr(model, key, post_data[key])
        db.session.add(model)
        db.session.commit()

        return model
