from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import POSTGRES_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'''
    postgresql://{POSTGRES_CONFIG["username"]}:{POSTGRES_CONFIG["password"]}@localhost:{POSTGRES_CONFIG["port"]}/{POSTGRES_CONFIG["name"]}
'''.strip()
db = SQLAlchemy(app)


@app.route('/')
def index():
    return '<h1>The site is not implemented yet</h1>'


@app.route('/register')
def register_request():
    pass


@app.route('/remove')
def remove_request():
    pass


# TODO: think about the handlers logic
# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found"


@app.errorhandler(500)
def page_not_found(e):
    return "500 Internal Error"


if __name__ == '__main__':
    app.run(debug=True)

