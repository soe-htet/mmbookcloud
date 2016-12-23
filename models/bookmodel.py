
from db import db
from datetime import datetime
from models.membermodel import MemberModel
from flask import jsonify

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer)
    owner_name = db.Column(db.UnicodeText(128))
    book_name = db.Column(db.UnicodeText(256))
    book_type = db.Column(db.String(128))
    book_url = db.Column(db.String(80))
    book_preview = db.Column(db.String(80))
    author = db.Column(db.UnicodeText(256))
    description = db.Column(db.UnicodeText(1024))
    tags = db.Column(db.UnicodeText(1024))
    date = db.Column(db.DateTime)

    def __init__(self, owner_id, owner_name, book_name,book_type,book_url,book_preview,author,description,tags):
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.book_name = book_name
        self.book_type = book_type
        self.book_url = book_url
        self.book_preview = book_preview
        self.author = author
        self.description = description
        self.tags = tags;
        self.date = datetime.now()

    def json(self):
        return {
                'id': self.id,
                'owner_id': self.owner_id,
                'owner_name': self.owner_name,
                'owner': MemberModel.get_by_id(self.owner_id),
                'book_name': self.book_name,
                'book_type': self.book_type,
                'book_url': self.book_url,
                'book_preview': self.book_preview,
                'author': self.author,
                'description': self.description,
                'tags':self.tags,
                'date': self.date.strftime("%Y-%m-%d %H:%M:%S")
                }

    @classmethod
    def get_by_book_name(cls, book_name):
        return cls.query.filter_by(book_name=book_name).first()

    @classmethod
    def get_by_book_id(cls, id):
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

    @classmethod
    def getbooklist(cls,page):
        books = cls.query.paginate(page=page, per_page=2)
        return books


### paganation example
# users = User.query.paginate(page=2, per_page=20)
# next_users = users.next()
# prev_users = user.prev()
