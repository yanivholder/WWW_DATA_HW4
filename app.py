import telegram
from flask import Flask, request, Response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_cors import cross_origin

from telegram_bot import bot
from models import db, User, Poll, Answer, Admin
from config import POSTGRES_CONFIG, flask_secret_key

app = Flask(__name__)
app.secret_key = flask_secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(admin_name):
    return Admin.get_by_name(admin_name)


app.config['SQLALCHEMY_DATABASE_URI'] = f'''
    postgresql://{POSTGRES_CONFIG["username"]}:{POSTGRES_CONFIG["password"]}@localhost:{POSTGRES_CONFIG["port"]}/{POSTGRES_CONFIG["name"]}
'''.strip()

db.init_app(app)


@app.route('/register')
def register_request():
    try:
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
    except:
        return Response("Unexpected error", status=500)


@app.route('/remove')
def remove_request():
    try:
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
    except:
        return Response("Unexpected error", status=500)


def broadcast_poll(recipients: list, poll_id, poll_content, poll_answers):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{ans.replace('_', ' ')}", callback_data=f"/answer {ans} {poll_id}")]
        for ans in poll_answers])

    for recip in recipients:
        try:
            bot.send_message(chat_id=recip, text=poll_content, reply_markup=markup)
        except telegram.error.TelegramError:
            Poll.remove_poll(poll_id)
            return False
    return True


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def filter_users_by_answers(predicate: str) -> list:  # get back only users after filter by pred
    all_users = User.get_all_active_users()
    if predicate is None or not predicate:
        return all_users
    else:
        pred = [(int(qna.split(',')[0]), qna.split(',')[1].replace(' ', '_')) for qna in predicate.split('$') if qna != '']
        partial_group_users = all_users
        for qna in pred:
            partial_group_users = intersection(partial_group_users, Answer.users_that_answered_a_on_q(qna[0], qna[1]))
        return partial_group_users


@app.route('/answer')
def handle_answer_poll():
    """Used when user responds to a poll via telegram and send it's answer"""
    try:
        requested_answer = request.args['answer']
        answered_poll = request.args['poll']
        chat_id = request.args['chat_id']

        if not User.is_active(chat_id):
            return Response("You are not a registered user.\nIn order to answer polls you have to register.", status=401)

        poll_pos_ans = Poll.get_poll_all_possible_answers(answered_poll)
        if len(poll_pos_ans) == 0:
            return Response("There's no such poll.\n(it was cancelled)", status=404)

        user_ans = Answer.get_current_user_answer(chat_id, answered_poll)
        if user_ans is None:
            return Response("You are not authorized to answer this poll.", status=401)

        if user_ans != "N.A":
            return Response("You have already answered this poll.\nYou may only answer once.", status=401)

        if requested_answer not in poll_pos_ans or requested_answer == "N.A":
            return Response("This in not a possible answer for this poll.", status=400)

        Answer.update_user_answer(chat_id, answered_poll, requested_answer)
        return Response(f"We have received your response:\n({requested_answer.replace('_', ' ')})\nThank you for participating", status=200)
    except:
        return Response("Unexpected error", status=500)


@app.route('/add_poll')
@cross_origin()
# @login_required
def handle_add_poll():
    try:
        new_poll_content = request.headers['question']
        new_poll_answers = [request.headers['answer1'], request.headers['answer2']]  # compulsory answers
        for pos_ans in [request.headers['answer3'], request.headers['answer4']]:  # voluntary answers
            if pos_ans != "":
                new_poll_answers += [pos_ans]

        for i in range(len(new_poll_answers)):
            new_poll_answers[i] = new_poll_answers[i].replace(' ', '_')

        predicate = request.headers['filters']  # this is a list of previous polls and specific answers to filter by

        relevant_users = filter_users_by_answers(predicate)
        new_poll_id = Poll.add_new_poll_and_default_answers(new_poll_content, new_poll_answers, relevant_users)

        if broadcast_poll(relevant_users, new_poll_id, new_poll_content, new_poll_answers):
            return Response("Poll successfully sent to all relevant users", status=200)
        else:
            return Response("Failed to send poll to some of the users,\nCancelled poll for all users that received it", status=500)
    except:
        return Response("Unexpected error", status=500)


@app.route('/remove_poll/<poll_id>')
@cross_origin()
# @login_required
def handle_remove_poll(poll_id):
    try:
        if Poll.remove_poll(poll_id):
            return Response("Poll successfully removed", status=200)
    except Exception as e:
        return Response(f"Unexpected error", status=500)

@app.route('/get_polls')
@cross_origin()
# @login_required
def handle_get_polls():  # return dict {questions: list[]} where list is of (poll_id, poll_content)
    """ Return all polls recorded in system, for displaying in UI """
    try:
        return {'questions': Poll.get_all_polls_id_and_content()}
    except:
        return Response("Unexpected error", status=500)


@app.route('/poll_info/<poll_id>')
@cross_origin()
# @login_required
def handle_get_info_about_poll(poll_id) -> list[[str, int]]:
    """ Return answer count for each possible answer of the poll with id <poll_id> """
    try:
        if int(poll_id) not in Poll.get_all_polls_id():
            return {}
        return {'data': Answer.get_poll_answer_count(poll_id)}
    except:
        return Response("Unexpected error", status=500)


@app.route('/add_admin')
@cross_origin()
def handle_add_admin():
    try:
        new_admin_name = request.headers['username']
        new_admin_password = request.headers['password']
        if Admin.is_registered(new_admin_name):
            return Response("This admin username is taken.\nPlease select a different name.", status=409)
        Admin.register_new_admin(new_admin_name, new_admin_password)
        return Response(f"Successfully registered new admin - {new_admin_name}.", status=200)
    except:
        return Response("Unexpected error", status=500)


@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    try:
        existing_admin_name = request.headers['username']
        existing_admin_password = request.headers['password']
        admin = Admin.get_by_name(existing_admin_name)
        if admin is None:
            return Response("No admin under this username.", status=404)
        if Admin.authenticate_admin(existing_admin_name, existing_admin_password):
            login_user(admin)
            return Response(f"Admin {existing_admin_name} Successfully logged-in.", status=200)
        else:
            return Response(f"Admin {existing_admin_name} logging-in failed.", status=401)
    except Exception as e:
        return Response("Unexpected error", status=500)

@app.route('/logout')
@cross_origin()
# @login_required
def logout():
    try:
        logout_user()
        return Response(f"Successfully logged-out.", status=200)
    except:
        return Response("Unexpected error", status=500)


@app.route('/get_all_admins')
@cross_origin()
# @login_required
def handle_get_admins():
    try:
        return {'admins': Admin.get_all_admin_names()}
    except:
        return Response("Unexpected error", status=500)


@app.route('/get_all_active_users')
@cross_origin()
# @login_required
def handle_get_users():
    try:
        return {'users': User.get_all_active_users()}
    except:
        return Response("Unexpected error", status=500)

# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return Response("404 Not Found", status=404)


@app.errorhandler(500)


def page_not_found(e):
    return Response("500 Internal Error", status=404)


if __name__ == '__main__':
    app.run(debug=True)
