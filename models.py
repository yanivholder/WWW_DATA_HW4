from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKeyConstraint, ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(64), unique=False, index=False)
    live = db.Column(db.Boolean(64), unique=False, index=False)

    def __repr__(self):
        return f'<User {self.username}'

    @staticmethod
    def is_registered(chat_id):
        """ checks whether chat_id is in the table Users, if so, return the current name under it, if not - none """
        user = db.session.query(User).filter_by(id=chat_id).first()
        if user is None:
            return None
        else:
            return user.username

    @staticmethod
    def is_active(chat_id):
        """ checks whether chat_id is in the table Users, if so, return the current name under it, if not - none """
        user = db.session.query(User).filter_by(id=chat_id).first()
        if user is None:
            return False
        else:
            return user.live

    @staticmethod
    def activate(chat_id):
        db.session.query(User).filter(User.id == chat_id).update({'live': True})
        db.session.commit()

    @staticmethod
    def register_new(chat_id, user_name):
        """ does the registration in to the DB for first time registration """
        db.session.add(User(id=chat_id, username=user_name, live=True))
        db.session.commit()

    @staticmethod
    def register_update(chat_id, user_name):
        """ does the registration in to the DB for non-first time registration """
        db.session.query(User).filter(User.id == chat_id).update({'username': user_name})
        db.session.commit()

    @staticmethod
    def remove(chat_id):
        # to_be_removed = db.session.query(User).filter(User.id == chat_id).first()
        # db.session.delete(to_be_removed)
        db.session.query(User).filter(User.id == chat_id).update({'live': False})
        db.session.commit()


class Poll(db.Model):
    poll_unique_id_counter = 1
    __tablename__ = 'polls'
    poll_id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(64), unique=False, index=False, nullable=False)
    possible_answers = db.Column(db.String, unique=False, index=False, nullable=False)
    PrimaryKeyConstraint(poll_id)
    CheckConstraint(poll_id > 0)

    def __repr__(self):
        return f'<Poll {self.content}'

    @staticmethod
    def get_poll_all_possible_answers(poll_id):
        """ """
        pos_ans = db.session.query(Poll).filter_by(poll_id=poll_id).first()
        if pos_ans is None:
            return []
        else:
            return pos_ans.content.split(',')

    @staticmethod
    def get_all_polls():
        polls = db.session.query(Poll).filter_by().all()
        if polls is None:
            return []
        else:
            return [p.id for p in polls]

    @staticmethod
    def add_new_poll(new_poll_content, new_poll_answers) -> int:
        current_poll_id = Poll.poll_unique_id_counter
        Poll.poll_unique_id_counter += 1
        db.session.add(Poll(poll_id=current_poll_id, content=new_poll_content, possible_answers=new_poll_answers))
        return current_poll_id





class Answer(db.Model):
    __tablename__ = 'answers'
    user_id = db.Column(db.String, db.ForeignKey(User.id), unique=False)
    poll_id = db.Column(db.Integer, db.ForeignKey(Poll.poll_id), unique=False, index=False)
    answer = db.Column(db.String, unique=False, index=False)
    PrimaryKeyConstraint(user_id, poll_id)

    def __repr__(self):
        return f'<Admin {self.username}'

    @staticmethod
    def get_current_answer(user_id, poll_id):
        return db.session.query(User).filter_by(user_id=user_id, poll_id=poll_id).first().answer

    @staticmethod
    def add_new_poll_default_answers(relevant_users, poll_id):
        """ """
        for usr in relevant_users:
            db.session.add(Answer(user_id=usr, poll_id=poll_id, answer="N.A"))
        db.session.commit()

    @staticmethod
    def update_user_answer(usr_id, poll_id, ans):
        """ before calling this, upper level should check that and is in <poll_id>'s possible answers """
        db.session.query(User).filter(Answer.user_id == usr_id, Answer.poll_id == poll_id).update({'answer': ans})
        db.session.commit()

    @staticmethod
    def get_poll_audience(poll_id):
        """ """
        relevant_users = db.session.query(Answer).filter_by(poll_id=poll_id).all()
        if relevant_users is None:
            return []
        else:
            return [row.user_id for row in relevant_users]


class Admin(db.Model):
    __tablename__ = 'admins'
    username = db.Column(db.String, primary_key=True, nullable=False)
    password = db.Column(db.String(64), unique=False, index=False, nullable=False)

    def __repr__(self):
        return f'<Admin {self.username}'

    @staticmethod
    def register_new_admin(user_name, pwd):
        """ Add another admin to the system """
        db.session.add(Admin(username=user_name, password=pwd))
        db.session.commit()

    @staticmethod
    def m1(chat_id):
        """ """
