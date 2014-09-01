"""Abstract base model class(es)."""


from peanuts.database import db


__all__ = ['Model']


class Model(db.Model):
    """A base model class."""
    __abstract__ = True

    def get_dictionary(self, verbosity='all'):
        """Returns a JSON-serializable dictionary representation of the model.

            This can and should be overridden on individual model classes,
            defining how to respond to different verbosities and/or fields
            that should never be returned to the frontend (e.g password).

            Kwargs:
                verbosity (str): A string indicating how much information
                    should be returned.  This accepts only 'all' and 'none'
                    unless the model base class stipulates otherwise.
                    (default='all')
        """
        return dict([
                (c.name, str(getattr(self, c.name)))
                for c in self.__table__.columns
            ]) if verbosity == 'all' else {}
