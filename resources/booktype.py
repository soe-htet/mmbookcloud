import werkzeug
from flask_restful import Resource,reqparse
from models.booktypemodel import booktypemodel


class booktype(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_type', type= str, required= True, help= "This field is must!")

    def get(self,username):
        tmp = booktypemodel.get_by_name(username)
        if tmp:
            return tmp
        else:
            return {'message', 'booktype not found'}, 404

    def post(self):
        data = booktype.parser.parse_args()
        if booktypemodel.get_by_name(data['book_type']):
            return {'message':'type already exit'}, 400

        tmp = booktypemodel(data['book_type'])
        try:
            tmp.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        return tmp.json(), 201

    def delete(self, name):
        if booktypemodel.get_by_name(name) is None:
            return {'message','type doesn\'t exit'}, 404
        tmp = booktypemodel.get_by_name(name)
        tmp.delete_from_db()
        return {'message','type deleted'}, 200

class booktypelist(Resource):
    def get(self):
        return {'booktypes': [x.json() for x in booktypemodel.query.all()]}


