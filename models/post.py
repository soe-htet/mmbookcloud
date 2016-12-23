from db import db
import json
from datetime import datetime
from models.SellerModel import SellerModel

class postModel(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    noofkg = db.Column(db.Integer)
    priceperkg = db.Column(db.String(80))
    ava_date = db.Column(db.Date)
    desc = db.Column(db.String(200))
    _from = db.Column(db.String(80))
    _to = db.Column(db.String(80))
    status = db.Column(db.String(80))
    post_date = db.Column(db.DateTime)

    def __init__(self, user_id,noofkg,priceperkg,ava_date,desc,_from,_to,status):
        self.user_id = user_id
        self.noofkg = noofkg
        self.priceperkg = priceperkg
        self.ava_date = datetime.fromtimestamp(ava_date/1000.0)
        self.desc = desc
        self._from = _from
        self._to = _to
        self.status = status
        self.post_date = datetime.now()

    def json(self):
        return {'owner': SellerModel.get_by_id(self.user_id),
                'user_id':self.user_id,
                'noofkg': self.noofkg,
                'priceperkg': self.priceperkg,
                'ava_date': self.ava_date.strftime("%Y-%m-%d"),
                'desc': self.desc,
                '_from': self._from,
                '_to': self._to,
                'status': self.status,
                'post_date': self.post_date.strftime("%Y-%m-%d %H:%M:%S")
                }

    @classmethod
    def get_by_user_id(cls, username_id):
        return cls.query.filter_by(username_id=username_id)

    @classmethod
    def get_by_post_id(cls, post_id):
        return cls.query.filter_by(id=post_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


