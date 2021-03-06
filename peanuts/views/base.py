"""Base view(s) which parse a model from a controller into a request and a
    request into a dictionary for the controller.
"""


from needs import needs

from flask import request, jsonify, session
from flask.ext.classy import FlaskView

from peanuts.lib.auth import app_need, csrf_need


__all__ = ['BaseView', 'BaseRestView']


class BaseView(FlaskView):
    """A base class for RESTful views."""
    Controller = None

    @property
    def request(self):
        """Returns the flask request object."""
        return request

    @property
    def session(self):
        """Returns the flask session object."""
        return session

    @property
    def controller(self):
        """An instance of the controller class at self.Controller."""
        return self.Controller()

    @property
    def data(self):
        """The request data."""
        return self.request.get_json()

    @property
    def verbosity(self):
        """The verbosity of the return dictionary as dictated by the url
            parameter.
        """
        return self.request.args.get('verbosity', 'none')

    def jsonify(self, data):
        """Makes a nice json response."""
        return jsonify(
            data=(
                [
                    d.get_dictionary(self.verbosity)
                    if hasattr(d, 'get_dictionary') else
                    d
                    for d in data
                    ] if isinstance(data, list) else
                data.get_dictionary(self.verbosity)
                if hasattr(data, 'get_dictionary') else
                data
                ),
            verbosity=self.verbosity,
            url=self.request.url,
            method=self.request.method
            )

    @needs(app_need)
    @needs(csrf_need)
    def before_request(self, name, *args, **kargs):
        """This is wrapped in an app_need since only registered apps may
            access these endpoint.
        """
        pass

class BaseRestView(BaseView):
    """A base class for RESTful views."""
    def index(self):
        """Gets a list of objects from the controller."""
        return self.jsonify(self.controller.index(self.request.args))

    def get(self, id_):
        """Gets an individual object from the controller."""
        return self.jsonify(self.controller.get(int(id_)))

    def post(self):
        """Posts a new object to the controller."""
        return self.jsonify(self.controller.post(self.data)), 201

    def put(self, id_):
        """Updates an existing model with new data."""
        return self.jsonify(self.controller.put(int(id_), self.data))

    def delete(self, id_):
        """Deletes an existing model."""
        self.controller.delete(int(id_))
        return self.jsonify({}), 204
