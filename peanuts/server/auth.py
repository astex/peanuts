from flask.ext.principal import Principal

def register(app):
    Principal(app)
