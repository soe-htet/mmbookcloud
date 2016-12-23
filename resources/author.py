import werkzeug
from flask_restful import Resource,reqparse
from models.authormodel import authormodel


class author(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('author_name', type= str, required= True, help= "This field is must!")

    def get(self,username):
        tmp = authormodel.get_by_name(username)
        if tmp:
            return tmp
        else:
            return {'message', 'author not found'}, 404

    def post(self):
        data = author.parser.parse_args()
        if authormodel.get_by_name(data['author_name']):
            return {'message':'username already exit'}, 400

        tmp = authormodel(data['author_name'])
        try:
            tmp.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        return tmp.json(), 201

    def delete(self, username):
        if authormodel.get_by_name(username) is None:
            return {'message','account doesn\'t exit'}, 404
        tmp = authormodel.get_by_name(username)
        tmp.delete_from_db()
        return {'message','account deleted'}, 200

class authorlist(Resource):
    def get(self):
        return {'authors': [x.json() for x in authormodel.query.all()]}


