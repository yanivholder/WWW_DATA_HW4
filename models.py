from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return f'<User {self.username}'

    def is_registered(chat_id):
        """ checks whether chat_id is in the table Users, if so, return the current name under it, if not - none """
        user = db.session.query(User).filter(User.id == chat_id)
        if user is None:
            return None
        else:
            return user.username

    def register_new(chat_id, user_name):
        """ does the registration in to the DB for first time registration """
        db.session.add(User(id=chat_id, username=user_name))
        db.session.commit()

    def register_update(chat_id, user_name):
        """ does the registration in to the DB for non-first time registration """
        db.session.query(User).filter(User.id == chat_id).update({'username': user_name})
        db.session.commit()

