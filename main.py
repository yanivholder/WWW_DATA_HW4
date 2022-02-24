import threading
import logging
import os
import subprocess
from multiprocessing import Process
from models import Admin

import sqlalchemy.testing.util
from sqlalchemy import engine
from sqlalchemy_utils import database_exists, create_database

from app import app
from models import db
from telegram_bot import run_telegram_bot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


# def table_exists(name):
#     return engine.dialect.has_table(engine, name)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            print("db doesn't exists. creating db:")
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            with app.app_context():
                db.create_all()
                db.session.commit()
                Admin.register_super_admin(db)
        else:
            # with app.app_context():
                # db.drop_all()
                # db.create_all()
                # db.session.commit()
            print("db exists")
        app.run()


class TelegramThread(threading.Thread):
    def run(self) -> None:
        run_telegram_bot()


def run_react():
    os.chdir("./react-app")  # change this before submission
    subprocess.check_call('npm install', shell=True)
    subprocess.check_call('npm start', shell=True)


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()

    bot_thread = TelegramThread()
    bot_thread.start()

    # react_process = Process(target=run_react)
    # react_process.start()



