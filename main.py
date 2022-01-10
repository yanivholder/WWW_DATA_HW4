import threading
import logging

import sqlalchemy.testing.util
from sqlalchemy_utils import database_exists, create_database

from app import app
from models import db
from telegram_bot import run_telegram_bot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            with app.app_context():
                db.create_all()
                db.session.commit()
        else:
            with app.app_context():
                db.drop_all()
                db.create_all()
                db.session.commit()
            print("db exists")
        app.run()


class TelegramThread(threading.Thread):
    def run(self) -> None:
        run_telegram_bot()


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()
    bot_thread = TelegramThread()
    bot_thread.start()



