"""Base view(s) which parse a model from a controller into a request and a 
    request into a dictionary for the controller.
"""


from flask import request, jsonify, json
from flask.ext.classy import FlaskView


__all__ = ['BaseRestView']


class BaseRestView(FlaskView):
    """A base class for RESTful views."""
    Controller = None

    @property
    def controller(self):
        """An instance of the controller class at self.Controller."""
        return self.Controller()

    @property
    def verbosity(self):
        """The verbosity of the return dictionary as dictated by the url
            parameter.
        """
        return request.args.get('verbosity', 'none')

    @property
    def data(self):
        """The request data."""
        return request.get_json()

    def jsonify(self, data):
        """Makes a nice json response."""
        return jsonify(
            data = [
                    json.dumps(d.get_dictionary(self.verbosity))
                    for d in data
                ] if isinstance(data, list) else
                json.dumps(data.get_dictionary(self.verbosity)),
            verbosity = self.verbosity,
            url = request.url
        )

    def index(self):
        """Gets a list of objects from the controller."""
        return self.jsonify(self.controller.index(
                request.args
            ))
