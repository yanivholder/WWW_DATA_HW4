import threading
from sqlalchemy_utils import database_exists, create_database

from app import app
from models import db
from telegram_bot import run_telegram_bot


class FlaskThread(threading.Thread):
    def run(self) -> None:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
        else:
            print("db exists")
        app.run()


class TelegramThread(threading.Thread):
    def run(self) -> None:
        run_telegram_bot()


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()
    # bot_thread = TelegramThread()
    # bot_thread.start()

    db.create_all()

    from models import User

    admin = User(username='admin', id=1)
    guest = User(username='guest', id=2)

    from app import db
    # db.session.add(admin)
    # db.session.add(guest)
    # db.session.commit()
    print(User.query.filter_by(username='admin'))
