from flask import Flask, request, Response
from models import db, User

from config import POSTGRES_CONFIG

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = f'''
#     postgresql://{POSTGRES_CONFIG["username"]}:{POSTGRES_CONFIG["password"]}@localhost:{POSTGRES_CONFIG["port"]}/{POSTGRES_CONFIG["name"]}
# '''.strip()
#
# db.init_app(app)

@app.route('/')
def index():
    return '<h1>The site is not implemented yet</h1>'


@app.route('/register')
def register_request():
    # TODO - what if request.method is not GET? should we return error? or not deal with this case
    new_user_name = request.args['username']
    chat_id = request.args['chat_id']

    old_user_name = User.is_registered(chat_id)

    if old_user_name is not None:  # existing user, either live or not
        if old_user_name == new_user_name:
            if User.is_active(chat_id):
                return Response("You've already registered under this username.", status=403)
            else:  # this is a previously registered user under same name, now coming back
                User.activate(chat_id)
                return Response("Welcome back!\nWere glad you chose to re-join us.", status=200)

        else:
            if User.is_active(chat_id):
                User.register_update(chat_id, new_user_name)
                return Response(f"Successfully changed your username.\nChanged from {old_user_name} to {new_user_name}.", status=200)
            else:  # returning user under different name.
                User.activate(chat_id)
                User.register_update(chat_id, new_user_name)
                return Response(f"Different name, same game.\nGood to have you back.", status=200)

    else: # old_user_name is None -> this is a brand new user
        User.register_new(chat_id, new_user_name)
        return Response(f"Welcome aboard, {new_user_name}.", status=200)


@app.route('/remove')
def remove_request():
    requested_user_name = request.args['username']
    chat_id = request.args['chat_id']

    existing_user_name = User.is_registered(chat_id)

    if existing_user_name is not None and not User.is_active(chat_id):
        return Response(f"This user was already removed.", status=200)

    if existing_user_name is not None:
        if existing_user_name == requested_user_name:
            User.remove(chat_id)
            return Response(f"Successfilly removed your user \"{requested_user_name}\" from system.", status=200)
        else:
            return Response(f"You are registered under the username {existing_user_name}.\nYou are not authorized to remove {requested_user_name}.", status=401)

    else:  # old_user_name is None
        return Response(f"You are not registered in the system.", status=400)


# TODO: think about the handlers logic
# TODO: maybe add render_template

# Polling functions

######################################################### TODO: erase
TMP = ([],  # filters
       "What color are the skies",  # question
       ["White",
        "Blue",
        "Brown",
        "Yellow"])  # answers


@app.route('/test')
def test():
    import time
    return {'time': time.time()}

######################################################### \erase


@app.route('/poll')
def make_new_poll():
    filters, question, answers = TMP


@app.route('/poll_info')
def get_info_about_poll():
    filters, question, answers = TMP

# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found"


@app.errorhandler(500)
def page_not_found(e):
    return "500 Internal Error"


if __name__ == '__main__':
    app.run(debug=True)

