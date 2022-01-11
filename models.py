from flask_sqlalchemy import SQLAlchemy

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
            return None
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
