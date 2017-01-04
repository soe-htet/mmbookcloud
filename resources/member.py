import werkzeug
from flask_restful import Resource,reqparse
from flask import redirect,url_for, make_response
from models.membermodel import MemberModel
import base64

class Member(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type= str, required= True, help= "This field is must!")
    parser.add_argument('password', type= str, required= True, help= "This field is must!")
    parser.add_argument('email', type= str, required= True, help= "This field is must!")

    def get(self,username):
        member = MemberModel.get_by_name(username)
        if member:
            return member
        else:
            return {'message', 'member not found'}, 404

    def post(self):
        data = Member.parser.parse_args()
        if MemberModel.get_by_name(data['username']):
            return {'message':'username already exit'}, 400

        if MemberModel.get_by_name(data['username']):
            return {'message':'email already registered'}, 400

        member = MemberModel(data['username'],data['email'],data['password'])
        try:
            member.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        return member.json(), 201

    def delete(self, username):
        if MemberModel.get_by_name(username) is None:
            return {'message','account doesn\'t exit'}, 404
        member = MemberModel.get_by_name(username)
        member.delete_from_db()
        return {'message','account deleted'}, 200

class memberList(Resource):
    def get(self):
        return {'members': [x.json() for x in MemberModel.query.all()]}


class memberLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type= str, required= True, help= "This field is must!")
    parser.add_argument('password', type= str, required= True, help= "This field is must!")
    parser.add_argument('mobile',type=bool, required=False)
    def post(self):
        data = memberLogin.parser.parse_args()
        member = MemberModel.get_by_email(data['email'])
        if member:
            if member.password == base64.b64encode(data['password'], 'utf-8'):
                if data['mobile'] == None:
                    resp = make_response(url_for('upload_file1'))
                    resp.set_cookie('username', member.username)
                    resp.set_cookie('id', str(member.id))
                    return resp
                else:
                    return member.json(), 200

            else:
                return {'message': 'incorrect email or password'},400

        return {'message': 'user not found'},404
