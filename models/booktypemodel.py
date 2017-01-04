
from db import db

class booktypemodel(db.Model):
    __tablename__ = 'booktypes'

    id = db.Column(db.Integer, primary_key = True)
    booktype= db.Column(db.String)

    def __init__(self, book_type):
        self.booktype = book_type

    def json(self):
        return {
                'id': self.id,
                'book_type': self.booktype,
                }

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(booktype=name).first()

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
