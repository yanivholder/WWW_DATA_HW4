from flask import Flask
from config import POSTGRES_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'''
    postgresql://{POSTGRES_CONFIG["username"]}:{POSTGRES_CONFIG["password"]}@localhost:{POSTGRES_CONFIG["port"]}/{POSTGRES_CONFIG["name"]}
'''.strip()


@app.route('/')
def index():
    return '<h1>The site is not implemented yet</h1>'


if __name__ == '__main__':
    app.run(debug=True)
