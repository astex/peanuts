"""A simple script to run peanuts."""


from peanuts import create_app


if __name__ == '__main__':
    app = create_app('../config/main.py')
    app.run()
