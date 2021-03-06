
from db import db
from datetime import datetime
from models.membermodel import MemberModel

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer)
    owner_name = db.Column(db.String)
    book_name = db.Column(db.String)
    book_type = db.Column(db.String(128))
    book_url = db.Column(db.String(80))
    book_preview = db.Column(db.String(80))
    author = db.Column(db.String)
    description = db.Column(db.String)
    tags = db.Column(db.String)
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
        books = cls.query.order_by(cls.date.desc()).paginate(page=page, per_page=3)
        return books

    @classmethod
    def getbooklistbyname(cls,page,name):
        books = cls.query.filter_by(book_name=name).paginate(page=page, per_page=2)
        return books

    @classmethod
    def getbooklistbyauthor(cls,page,author):
        books = cls.query.filter_by(author=author).paginate(page=page, per_page=2)
        return books

    @classmethod
    def getbooklistbytype(cls,page,type):
        books = cls.query.filter_by(book_type=type).paginate(page=page, per_page=2)
        return books

    @classmethod
    def getbooksbyfilter(cls,page,filter_name):
        books = cls.query.filter((cls.book_type==filter_name) | (cls.author==filter_name)).order_by(cls.date.desc()).paginate(page=page, per_page=2)
        return books


    @classmethod
    def booksearch(cls,page,name):
        tmp = '%'
        tmp2 = tmp + name + tmp
        books = cls.query.filter(cls.book_name.ilike(tmp2)).order_by(cls.date.desc()).paginate(page=page, per_page=2)
        return books

### paganation example
# users = User.query.paginate(page=2, per_page=20)
# next_users = users.next()
# prev_users = user.prev()
