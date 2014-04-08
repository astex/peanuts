import os
here = os.path.abspath( os.path.dirname( __file__ ) )

DEBUG = True

SERVER_HOST = os.environ.get('SERVER_HOST') or '0.0.0.0'
SERVER_PORT = os.environ.get('SERVER_PORT') or 5001

SECRET_KEY = '|\xe2Q&\xe0\x81_\x11\xb1\xb0!\xc3\x0f\xb6\xd0\x00\x10YO\xf5%r\tN'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://'
