import werkzeug
from flask_restful import Resource,reqparse,url_for
from models.SellerModel import SellerModel
import os
from flask import Flask,send_from_directory,redirect,request


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'imgs/'

class Seller(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type= str, required= True, help= "This field is must!")
    parser.add_argument('password', type= str, required= True, help= "This field is must!")
    parser.add_argument('email', type= str, required= True, help= "This field is must!")
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='imgs')
    parser.add_argument('phoneno', type= str, required= True, help= "This field is must!")
    parser.add_argument('phstatus', type= bool, required= True, help= "This field is must!")

    def get(self,username):
        seller = SellerModel.get_by_name(username)
        if seller:
            return seller
        else:
            return {'message', 'seller not found'}, 404

    def post(self):
        data = Seller.parser.parse_args()
        if SellerModel.get_by_name(data['username']):
            return {'message':'username already exit'}, 400

        img_url = ''
        f = request.files['file']
        if f:
            import requests
            url = 'http://burmesesoungs.com/mmnet/imgup.php?username=' + data['username'].lower()
            files = {'file': f}
            response = requests.post(url, files=files)
            img_url = "http://www.burmesesoungs.com/mmnet/profile/" + data['username'].lower()+".jpg"
        print(img_url)

        seller = SellerModel(data['username'],data['password'],data['email'],img_url,data['phoneno'],data['phstatus'])
        try:
            seller.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        return seller.json(), 201

    def delete(self, username):
        if SellerModel.get_by_name(username) is None:
            return {'message','account doesn\'t exit'}, 404
        seller = SellerModel.get_by_name(username)
        seller.delete_from_db()
        return {'message','account deleted'}, 200

class sellerList(Resource):
    def get(self):
        return {'sellers': [x.json() for x in SellerModel.query.all()]}


class sellerLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type= str, required= True, help= "This field is must!")
    parser.add_argument('password', type= str, required= True, help= "This field is must!")
    def post(self):
        data = sellerLogin.parser.parse_args()
        seller = SellerModel.get_by_name(data['username'])
        if seller:
            if seller.password == data['password']:
                return seller.json(), 200
            else:
                return {'message': 'login fail'},400

        return {'message': 'user not found'},404
