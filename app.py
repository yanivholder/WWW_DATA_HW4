from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import crud

from config import POSTGRES_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'''
    postgresql://{POSTGRES_CONFIG["username"]}:{POSTGRES_CONFIG["password"]}@localhost:{POSTGRES_CONFIG["port"]}/{POSTGRES_CONFIG["name"]}
'''.strip()

db.init_app(app)

@app.route('/')
def index():
    return '<h1>The site is not implemented yet</h1>'


@app.route('/register')
def register_request():
    # TODO - what if request.method is not GET? should we return error? or not deal with this case
    new_user_name = request.args['user_name']
    chat_id = request.args['ChatId']

    old_user_name = User.is_registered(chat_id)

    if old_user_name is not None:
        if old_user_name == new_user_name:
            return Response("You've already registered under this username.", status=403)
        else:
            User.register_update(chat_id, new_user_name)
            return Response(f"Successfully changed your username from {old_user_name} to {new_user_name}.", status=400)

    else: # old_user_name is None
        User.register_new(chat_id, new_user_name)
        return Response(f"Welcome aboard, {new_user_name}.", status=400)

    pass


@app.route('/remove')
def remove_request():
    pass


# TODO: think about the handlers logic
# TODO: maybe add render_template
# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found"


@app.errorhandler(500)
def page_not_found(e):
    return "500 Internal Error"


if __name__ == '__main__':
    app.run(debug=True)

