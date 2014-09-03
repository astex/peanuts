"""A library for dealing with classes."""


from functools import wraps


__all__ = ['methodize']


def methodize(dec):
    """Wraps a function decorator so it can wrap methods."""

    def adapt(f):
        @wraps(f)
        def decorated(self, *args, **kargs):
            @dec
            def g(*a, **k):
                return f(self, *a, **k)

            return g(*args, **kargs)
        return decorated
    return adapt
