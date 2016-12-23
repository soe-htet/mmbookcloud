
from db import db
import base64

class MemberModel(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.UnicodeText(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    confirmed = db.Column(db.Boolean)

    def __init__(self, username,email,password):
        self.username = username
        self.password = base64.b64encode(bytes(password, 'utf-8'))
        self.email = email
        self.confirmed = False

    def json(self):
        return {
                'id': self.id,
                'username': self.username,
                'password': self.password.decode(),
                'email': self.email,
                'confirmed': self.confirmed,
                }

    @classmethod
    def get_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        model = cls.query.filter_by(id=id).first()
        if model:
            return model.json()
        return {'user':'null'}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
