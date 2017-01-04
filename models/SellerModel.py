
from db import db

class SellerModel(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    pic = db.Column(db.String(80))
    phoneno = db.Column(db.String(15))
    phstatus = db.Column(db.Boolean)

    def __init__(self, username,password,email,pic,phoneno,phstatus):
        self.username = username
        self.password = password
        self.email = email
        self.pic = pic
        self.phoneno = phoneno
        self.phstatus = phstatus

    def json(self):
        return {
                'id': self.id,
                'username': self.username,
                'password': self.password,
                'email': self.email,
                'pic': self.pic,
                'phoneno': self.phoneno,
                'phstatus': self.phstatus
                }

    @classmethod
    def get_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

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
