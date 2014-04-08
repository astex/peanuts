from flask import request
from flask.ext.classy import FlaskView, route

class ViewRegistrar(object):

    VIEW_BASE = 'api'

    @classmethod
    def register(cls, app, views):

        for view in views:

            route_base = '/' + cls.VIEW_BASE + '/' + view.route_base
            view.register(app, route_base=route_base)

class BaseView(FlaskView):
    """A default generic view."""

    @property
    def request_data( self ):
        """Get incoming data from an API request."""

        data = getattr(request,'json',request.form)
        if hasattr(data,'to_dict'):
            # We don't want to leave the data as an ImmutableDict
            data = data.to_dict()

        return data or {}

    @property
    def request_args( self ):
        """Get URL parameters."""
        
        return request.args
