from .base import ViewRegistrar

from auth import AuthView

views = [ AuthView ]

def register( app ):
    ViewRegistrar.register(app, views)
