from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, desc, CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(64), unique=False, index=False)
    live = db.Column(db.Boolean(64), unique=False, index=False)
    answers = db.relationship('Answer', backref='user')

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
    def activate(chat_id, do_commit=True):
        db.session.query(User).filter(User.id == chat_id).update({'live': True})
        if do_commit:
            db.session.commit()

    @staticmethod
    def register_new(chat_id, user_name, do_commit=True):
        """ does the registration in to the DB for first time registration """
        db.session.add(User(id=chat_id, username=user_name, live=True))
        if do_commit:
            db.session.commit()

    @staticmethod
    def register_update(chat_id, user_name, do_commit=True):
        """ does the registration in to the DB for non-first time registration """
        db.session.query(User).filter(User.id == chat_id).update({'username': user_name})
        if do_commit:
            db.session.commit()

    @staticmethod
    def remove(chat_id, do_commit=True):
        # to_be_removed = db.session.query(User).filter(User.id == chat_id).first()
        # db.session.delete(to_be_removed)
        db.session.query(User).filter(User.id == chat_id).update({'live': False})
        if do_commit:
            db.session.commit()

    @staticmethod
    def get_all_active_users():
        all_active = db.session.query(User).filter_by(live=True).all()
        if all_active is None:
            return []
        else:
            return [usr.id for usr in all_active]


class Poll(db.Model):
    poll_unique_id_counter = 1
    __tablename__ = 'polls'
    poll_id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(64), unique=False, index=False, nullable=False)
    possible_answers = db.Column(db.String, unique=False, index=False, nullable=False)
    PrimaryKeyConstraint(poll_id)
    CheckConstraint(poll_id > 0)
    answers = db.relationship('Answer', backref='poll')

    def __repr__(self):
        return f'<Poll {self.content}'

    @staticmethod
    def get_poll_all_possible_answers(poll_id):
        """ """
        pos_ans = db.session.query(Poll).filter_by(poll_id=poll_id).first()
        if pos_ans is None:
            return []
        else:
            return pos_ans.possible_answers.split(',')

    @staticmethod
    def get_all_polls_id():
        polls = db.session.query(Poll).filter_by().all()
        if polls is None:
            return []
        else:
            return [p.poll_id for p in polls]

    @staticmethod
    def poll_exists(poll__id: int):
        poll = db.session.query(Poll).filter_by(poll_id=poll__id).first()
        if poll is None:
            return False
        else:
            return True


    @staticmethod
    def get_all_polls_id_and_content():
        polls = db.session.query(Poll).filter_by().all()
        if polls is None:
            return []
        else:
            return [(p.poll_id, p.content) for p in polls]

    @staticmethod
    def get_max_poll_id():
        max_poll = db.session.query(Poll).filter_by().order_by(desc(Poll.poll_id)).first()
        if max_poll is None:
            return 0
        else:
            return max_poll.poll_id



    @staticmethod
    def add_new_poll_and_default_answers(new_poll_content: str, new_poll_answers: list[str], relevant_users,
                                         do_commit=True) -> int:

        current_poll_id = Poll.get_max_poll_id()+1
        # create a string the concatenates the answers for saving in DB
        con_new_poll_answers = new_poll_answers[0] + ',' + new_poll_answers[1]  # compulsory answers
        for i in range(2, len(new_poll_answers)):                               # voluntary answers
            con_new_poll_answers += ',' + new_poll_answers[i]
        db.session.add(Poll(poll_id=current_poll_id, content=new_poll_content, possible_answers=con_new_poll_answers))

        Answer.add_new_poll_default_answers(relevant_users, current_poll_id, do_commit=False)
        if do_commit:
            db.session.commit()
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
    def get_current_user_answer(user_id, poll_id):
        ans = db.session.query(Answer).filter_by(user_id=user_id, poll_id=poll_id).first()
        if ans is None:
            return None
        else:
            return ans.answer

    @staticmethod
    def add_new_poll_default_answers(relevant_users, poll_id, do_commit=True):
        """ """
        for usr in relevant_users:
            db.session.add(Answer(user_id=usr, poll_id=poll_id, answer="N.A"))
        if do_commit:
            db.session.commit()

    @staticmethod
    def update_user_answer(usr_id, poll_id, ans, do_commit=True):
        """ before calling this, upper level should check that and is in <poll_id>'s possible answers """
        db.session.query(Answer).filter(Answer.user_id == usr_id, Answer.poll_id == poll_id).update({'answer': ans})
        if do_commit:
            db.session.commit()

    @staticmethod
    def get_poll_audience(poll_id):
        """ """
        relevant_users = db.session.query(Answer).filter_by(poll_id=poll_id).all()
        if relevant_users is None:
            return []
        else:
            return [row.user_id for row in relevant_users]

    @staticmethod
    def user_in_poll_audience(user__id, poll__id):
        """ """
        user = db.session.query(Answer).filter_by(poll_id=poll__id, user_id=user__id).first()
        if user is None:
            return False
        else:
            return True

    @staticmethod
    def users_that_answered_a_on_q(poll_id: int, specific_answer: str):
        specific_users = db.session.query(Answer).filter_by(poll_id=poll_id, answer=specific_answer).all()
        return [usr.user_id for usr in specific_users]

    @staticmethod
    def get_poll_answer_count(poll_id):
        ret = [("Did not answer yet", len(Answer.users_that_answered_a_on_q(poll_id, "N.A")))]
        for pos_ans in Poll.get_poll_all_possible_answers(poll_id):
            ret.append((pos_ans.replace('_', ' '), len(Answer.users_that_answered_a_on_q(poll_id, pos_ans))))

        return ret


class Admin(UserMixin, db.Model):
    # admin_unique_id_counter = 1000000
    __tablename__ = 'admins'
    username = db.Column(db.String, primary_key=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, index=False, nullable=False)
    # id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)


    def __repr__(self):
        return f'<Admin {self.username}'

    def get_id(self):
        return self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register_new_admin(user_name, pwd, do_commit=True):
        """ Add another admin to the system """
        # db.session.add(Admin(username=user_name, password=pwd, admin_id=Admin.admin_unique_id_counter))
        # Admin.admin_unique_id_counter += 1
        db.session.add(Admin(username=user_name, password=pwd))
        if do_commit:
            db.session.commit()

    @staticmethod
    def register_super_admin(input_db):
        """ Add first default admin to the system,
        different func because we need to specify db before app gives db by context """
        # input_db.session.add(Admin(username="admin", password="236369", admin_id=666))
        input_db.session.add(Admin(username="admin", password="236369"))
        input_db.session.commit()

    @staticmethod
    def authenticate_admin(user_name, pwd):
        """  """
        return db.session.query(Admin).filter_by(username=user_name).first().verify_password(pwd)

    @staticmethod
    def is_registered(admin_name):
        """ checks whether admin_name is in the table Users, if so, return the current name under it, if not - none """
        admin = db.session.query(Admin).filter_by(username=admin_name).first()
        if admin is None:
            return False
        else:
            return True

    @staticmethod
    def get_by_name(admin_name):
        return db.session.query(Admin).filter_by(username=admin_name).first()
