"""Error handling library."""


from werkzeug.exceptions import HTTPException
from flask import jsonify


__all__ = ['make_json_error']


def make_json_error(exception):
    """Raises a jsonic error intead of the default Werkzeug HTML."""
    from flask import request

    response = jsonify({
        'status': exception.code,
        'method': request.method,
        'url': request.url,
        'message': (
            exception.description if
            hasattr(exception, 'description') else
            str(exception)
            )
        }), exception.code if isinstance(exception, HTTPException) else 500

    return response
