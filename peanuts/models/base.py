from collections import iterable

from sqlalchemy import and_

from peanuts import db

class Model(db.Model):
    """A custom model class with some neat convenience methods and useful debug helpers."""

    __table_args__ = {
        'sqlite_autoincrement': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    dict_opts = dict(

        # Field names from self.columns to ignore.
        ignore = [],

        # Field names and relationship names to expand via to_dict().
        # Values can be either a string or a dict of the form { 'field': (field_name), 'dict_opts': (field_dict_opts) }.
        expand = [],

        # Non-db attributes/properties to include.
        include = [],

        # Attributes that should be forcibly excluded, even if these are included in dict_opts as passed in to to_dict().
        exclude = []

    )

    # Filters of the form { key: filter_function }.
    _filter_prefix = ''
    _filter_config = dict()

    @property
    def columns(self): return set(self.__table__.c.keys())

    def __repr__(self):
        """A useful debug representation of the model's primary key(s)."""

        keys = map( lambda key: key.name, self.__mapper__.primary_key )
        keys = ', '.join( map( lambda key: '{0}={1}'.format( key, getattr(self, key) ), keys ) )
        return '<{0} {1}>'.format( self.__class__.__name__, keys )

    def to_dict(self, dict_opts=None):
        """A dictionary representation of the model.

            By default, this includes all columns of the model.  Columns and properties can be explicitly included,
            excluded, expanded, ignored, ... via self.dict_opts or via the dict_opts argument.

            Kargs:
                dict_opts (dict): Dictionary options.  See the comments at Model.dict_opts for documentation.
        """

        dict_opts = dict_opts or {}
        if 'exclude' in dict_opts: dict_opts.pop('exclude')
        dict_opts.update( self.dict_opts )

        ignore_fields = dict_opts.get('ignore',[])
        expand_fields = dict_opts.get('expand',[])
        include_fields = dict_opts.get('include',[])
        exclude_fields = dict_opts.get('exclude',[])

        d = {}

        for name in self.columns:
            if name not in ignore_fields and name not in exclude_fields:
                d[name] = getattr(self, name)

        for name in include_fields:
            if name not in exclude_fields:
                d[name] = getattr(self, name, None)

        for field in expand_fields:

            if isinstance( field, dict ):
                expand_opts = field['dict_opts']
                field = field['field']
            else:
                expand_opts = None
            
            if field not in exclude_fields:

                value = getattr( self, field )

                if isinstance(value, dict):
                    d[field] = dict( [ (k, v.to_dict(expand_opts)) for k,v in value.iteritems() ] )
                elif isinstance(value, Iterable):
                    d[field] = [ v.to_dict(expand_opts) for v in value ]
                elif value:
                    d[field] = value.to_dict(expand_opts)

        return d

    @classmethod
    def get_filters(cls, data):

        """Returns a SQLAlchemy where condition parsed from cls._filter_config

            Args:
                data (dict): A dictionary with filter parameters of the form { prefix + key: value }.
        """

        filter_ = []

        if cls._filter_config:

            for key, value in data.iteritems():
                if key in cls._filter_config:
                    filter_fn = cls.config_filters.get(key)
                    if filter_fn is not None and hasatr(filer_fn, '__call__'): filter_.append(filter_fn(value))

        return and_( *filter_ )
