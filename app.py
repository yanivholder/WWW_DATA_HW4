from flask import Flask, request, Response
from models import db, User, Poll, Answer, Admin
from telegram_bot import broadcast

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
                return Response("You've already registered under this username.", status=409)
            else:  # this is a previously registered user under same name, now coming back
                User.activate(chat_id)
                return Response("Welcome back!\nWere glad you chose to re-join us.", status=200)

        else:
            if User.is_active(chat_id):
                User.register_update(chat_id, new_user_name)
                return Response(
                    f"Successfully changed your username.\nChanged from {old_user_name} to {new_user_name}.",
                    status=200)
            else:  # returning user under different name.
                User.activate(chat_id)
                User.register_update(chat_id, new_user_name)
                return Response(f"Different name, same game.\nGood to have you back.", status=200)

    else:  # old_user_name is None -> this is a brand new user
        User.register_new(chat_id, new_user_name)
        return Response(f"Welcome aboard, {new_user_name}.", status=200)


@app.route('/remove')
def remove_request():
    requested_user_name = request.args['username']
    chat_id = request.args['chat_id']

    existing_user_name = User.is_registered(chat_id)

    if existing_user_name is not None and not User.is_active(chat_id):
        return Response(f"This user was already removed.", status=400)

    if existing_user_name is not None:
        if existing_user_name == requested_user_name:
            User.remove(chat_id)
            return Response(f"Successfully removed your user \"{requested_user_name}\" from system.", status=200)
        else:
            return Response(
                f"You are registered under the username {existing_user_name}.\nYou are not authorized to remove {requested_user_name}.",
                status=401)

    else:  # old_user_name is None
        return Response(f"You are not registered in the system.", status=400)


@app.route('/answer')
def handle_answer_poll():
    """Used when user responds to a poll via telegram and send it's answer"""
    requested_answer = request.args['answer']
    answered_poll = request.args['poll']
    chat_id = request.args['chat_id']

    if not User.is_active(chat_id):
        return Response("You are not a registered user.\nIn order to answer polls you have to register.", status=401)

    if answered_poll not in Poll.get_all_polls():
        return Response("There's no such poll.", status=404)

    if chat_id not in Answer.get_poll_audience(answered_poll):
        return Response("You are not authorized to answer this poll.", status=401)

    if Answer.get_current_answer(chat_id, answered_poll) != "N.A":
        return Response("You have already answered this poll.\nYou may only answer once.", status=401)

    if requested_answer not in Poll.get_poll_all_possible_answers(answered_poll):
        return Response("This in not a possible answer for this poll.", status=400)

    Answer.update_user_answer(chat_id, answered_poll, requested_answer)
    return Response(f"We have received your response.\nThank you for participating", status=200)


@app.route('/poll')
def handle_add_poll():
    pass
    new_poll_content = request.args['poll_content']
    new_poll_answers = request.args['possible_answers']
    predicate = request.args['filter']  # this is a list of previous polls and specific answers to filter by

    new_poll_id = Poll.add_new_poll(new_poll_content, new_poll_answers)

    relevant_users = filter_users_by_answers(predicate)
    Answer.add_new_poll_default_answers(relevant_users, new_poll_id)

    broadcast(relevant_users, new_poll_content, new_poll_answers)








def get_count_per_answer(poll_id: int) -> dict[str, int]:  # dictionary with key = poll answer text, value = count
    pass


def filter_users_by_answers(pred: list[tuple[int, str]]) -> list:  # get back only users after filter by pred
    # pred is a list of tuples like [(Q1,A3), (Q3,A7)...] i.e, polls and specific answers as filters
    pass


def get_all_polls_sent() -> list[tuple[int, str]]:
    """ all polls recorded in system, for displaying in UI.
     returned in form of poll id, poll content """
    pass


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
