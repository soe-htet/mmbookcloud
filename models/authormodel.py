
from db import db

class authormodel(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key = True)
    author_name = db.Column(db.String)

    def __init__(self, author_name):
        self.author_name = author_name

    def json(self):
        return {
                'id': self.id,
                'author_name': self.author_name,
                }

    @classmethod
    def get_by_name(cls, author_name):
        return cls.query.filter_by(author_name=author_name).first()

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
