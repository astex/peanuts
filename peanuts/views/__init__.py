from peanuts.views import post, user


def register(app):
    post.PostView.register(app, route_base='/post/')
    user.UserView.register(app, route_base='/user/')
