"""A simple script to run peanuts."""


from peanuts import create_app

app = create_app('config/main.py')

if __name__ == '__main__':
    app.run()
