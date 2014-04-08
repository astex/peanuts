from flask import jsonify

from .classutils import instantiableclassproperty

class BaseError(Exception):
    """An Error class that can be raised either as the class or an instance.
    
        If more detail than the code and a generic message is desired, these can generally
        be instantiated in any which way.  For example,
        ```
            >>> raise ServerError
            Traceback (most recent call last):
                File "<stdin>", line 1, in <module>
            peanuts.lib.exception.ServerError: There was a problem.
            >>> raise ServerError('There was no problem.')
            Traceback (most recent call last):
                File "<stdin>", line 1, in <module>
            peanuts.lib.exception.ServerError: There was no problem.
        ```
        If raised in a Flask application context, their response property will be returned.
    """

    def __init__(self, msg=None):
        if isinstance(msg, (str, unicode)): self.msg = msg

    def __str__(self): return self.msg
    def __repr__(self): return "<{0} '{1}'>".format( self.__class__.__name__, self.msg )

    @classmethod
    def from_exception(cls, e): return cls(str(e))

class JsonError(BaseError):

    errors = {}

    def __init__(self, msg=None):
        super(JsonError, self).__init__(msg)
        if isinstance(msg, dict): self.errors = msg

    @instantiableclassproperty
    def response(self):
        r = jsonify(dict(
            errors = self.errors,
            msg = self.msg
        ))
        r.status_code = self.code
        return r

class ServerError(JsonError):
    code = 500
    msg = "There was a problem."
