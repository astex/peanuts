import peanuts

app = peanuts.create_app()

if __name__ == '__main__':

    app.run(
        host = app.config.get('SERVER_HOST'),
        port = app.config.get('SERVER_PORT'),
        debug = app.config.get('DEBUG')
    )
