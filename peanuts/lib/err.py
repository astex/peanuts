"""Error handling library."""


from werkzeug.exceptions import HTTPException
from flask import jsonify


__all__ = ['make_json_error']


def make_json_error(exception):
    """Raises a jsonic error intead of the default Werkzeug HTML."""
    response = jsonify(message=str(exception))
    response.status_code = (
        exception.code if isinstance(exception, HTTPException) else 500
        )
    return response
