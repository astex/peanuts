from peanuts.views import post, user, session


def register(app):
    post.PostView.register(app, route_base='/post/')
    user.UserView.register(app, route_base='/user/')
    session.SessionView.register(app, route_base='/session/')
