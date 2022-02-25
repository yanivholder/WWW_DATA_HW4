import telegram
from flask import Flask, request, Response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot import bot
from models import db, User, Poll, Answer, Admin
from flask_login import LoginManager, login_required, login_user, logout_user

from config import POSTGRES_CONFIG

app = Flask(__name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


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


def broadcast_poll(recipients: list, poll_id, poll_content, poll_answers):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{ans}", callback_data=f"/answer {ans} {poll_id}")]
        for ans in poll_answers])

    for recip in recipients:
        try:
            bot.send_message(chat_id=recip, text=poll_content, reply_markup=markup)
        except telegram.error.TelegramError:
            return False

    return True


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def filter_users_by_answers(predicate: str) -> list:  # get back only users after filter by pred
    all_users = User.get_all_active_users()
    if predicate is None or len(predicate) == 0:
        return all_users
    else:
        pred = [(int(qna.split(',')[0]), qna.split(',')[1]) for qna in predicate.split(' ')]
        partial_group_users = all_users
        for qna in pred:
            partial_group_users = intersection(partial_group_users, Answer.users_that_answered_a_on_q(qna[0], qna[1]))
        return partial_group_users


@app.route('/poll')
def handle_add_poll():
    new_poll_content = request.args['poll_content']
    new_poll_answers = request.args['possible_answers']
    predicate = request.args['filter']  # this is a list of previous polls and specific answers to filter by
    num_poss_ans = len(new_poll_answers.split(','))
    if num_poss_ans < 2 or num_poss_ans > 4:
        return Response("Illegal number of answers to requested Poll\nWe support 2-4 answers per Poll", status=403)

    i = request.args['itr']

    if int(i) == 1 or int(i) == 2:
        new_poll_content = f"question {i}"
        predicate = ""

    relevant_users = filter_users_by_answers(predicate)

    new_poll_id = Poll.add_new_poll_and_default_answers(new_poll_content, new_poll_answers, relevant_users)
    # Answer.add_new_poll_default_answers(relevant_users, new_poll_id)

    if broadcast_poll(relevant_users, new_poll_id, new_poll_content, new_poll_answers.split(',')):
        return Response("Poll successfully sent to all relevant users", status=200)
    else:
        return Response("Failed to send poll to some of the users", status=500)


@app.route('/answer')
def handle_answer_poll():
    """Used when user responds to a poll via telegram and send it's answer"""
    requested_answer = request.args['answer']
    answered_poll = request.args['poll']
    chat_id = request.args['chat_id']

    if not User.is_active(chat_id):
        return Response("You are not a registered user.\nIn order to answer polls you have to register.", status=401)

    if int(answered_poll) not in Poll.get_all_polls_id():
        return Response("There's no such poll.", status=404)

    if chat_id not in Answer.get_poll_audience(answered_poll):
        return Response("You are not authorized to answer this poll.", status=401)

    if Answer.get_current_answer(chat_id, answered_poll) != "N.A":
        return Response("You have already answered this poll.\nYou may only answer once.", status=401)

    if requested_answer not in Poll.get_poll_all_possible_answers(answered_poll):
        return Response("This in not a possible answer for this poll.", status=400)

    Answer.update_user_answer(chat_id, answered_poll, requested_answer)
    return Response(f"We have received your response:\n({requested_answer})\nThank you for participating", status=200)


@app.route('/add_admin')
def handle_add_admin():
    new_admin_name = request.args['admin_name']
    new_admin_password = request.args['admin_password']
    if Admin.is_registered(new_admin_name):
        return Response("This admin username is taken.\nPlease select a different name.", status=409)
    Admin.register_new_admin(new_admin_name, new_admin_password)
    return Response(f"Successfully registered new admin - {new_admin_name}.", status=200)


@app.route('/check_admin')
def handle_check_admin():
    existing_admin_name = request.args['admin_name']
    existing_admin_password = request.args['admin_password']
    if not Admin.is_registered(existing_admin_name):
        return Response("No admin under this username.", status=404)
    if Admin.authenticate_admin(existing_admin_name, existing_admin_password):
        return Response(f"Admin {existing_admin_name} Successfully authenticated.", status=200)
    else:
        return Response(f"Admin {existing_admin_name} authentication failed.", status=401)


def get_count_per_answer(poll_id: int) -> dict[str, int]:  # dictionary with key = poll answer text, value = count
    pass


@app.route('/get_polls')
@login_required
def handle_get_polls():  # return dict {questions: list[]} where list is of (poll_id, poll_content)
    """ Return all polls recorded in system, for displaying in UI """
    return {'questions': Poll.get_all_polls_id_and_content()}


@app.route('/poll_info/<poll_id>')
@login_required
def handle_get_info_about_poll(poll_id) -> dict[str: int]:
    """ Return answer count for each possible answer of the poll with id <poll_id> """
    if poll_id not in Poll.get_all_polls_id():
        return {}
    return Answer.get_poll_answer_count(poll_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    existing_admin_name = request.args['admin_name']
    existing_admin_password = request.args['admin_password']
    admin = Admin.get_by_name(existing_admin_name)
    if admin is None:
        return Response("No admin under this username.", status=404)
    if Admin.authenticate_admin(existing_admin_name, existing_admin_password):
        login_user(admin)
        return Response(f"Admin {existing_admin_name} Successfully logged-in.", status=200)
    else:
        return Response(f"Admin {existing_admin_name} logging-in failed.", status=401)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return Response(f"Successfully logged-out.", status=200)


# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return Response("404 Not Found", status=404)


@app.errorhandler(500)
def page_not_found(e):
    return Response("500 Internal Error", status=404)

QUESTIONS = [
    (1, "What is your eyes color"),
    (2, "Do you love apples"),
    (3, "How much legs 4 spiders and two people have?")
]

############################################### TODO: erase
@app.route('/test/get_polls')
def test_get_polls():
    return {"questions": QUESTIONS}


@app.route('/test/poll_info/1')
def test_poll_info():
    return {"data": [("White", 3), ("Blue", 5), ("Brown", 0), ("Yellow", 2), ("N/A", 23)]}


@app.route('/test/login')
def test_login():
    if request.headers["username"] == "yaniv" and request.headers["password"] == "123":
        return Response(status=200)
    else:
        return Response(status=400)

@app.route('/test/add_admin')
def test_add_admin():
    return Response(status=200)

@app.route('/test/add_poll')
def test_add_poll():
    print(request.headers)
    return Response(status=200)
###################################################### \erase

if __name__ == '__main__':
    app.run(debug=True)
