from peanuts.views.post import PostView


def register(app):
    PostView.register(app, route_base='/post/')
