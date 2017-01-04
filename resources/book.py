import werkzeug
from flask_restful import Resource,reqparse,url_for
from datetime import datetime
from models.bookmodel import BookModel
import os
from flask import Flask,request,jsonify


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'imgs/'

class book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_name', type= str, required= True, help= "This field is must!")
    parser.add_argument('book_type', type= str, required= True, help= "This field is must!")
    parser.add_argument('author', type= str, required= True, help= "This field is must!")
    parser.add_argument('pdf', type=werkzeug.datastructures.FileStorage, location='imgs')
    parser.add_argument('img', type=werkzeug.datastructures.FileStorage, location='imgs')
    parser.add_argument('description', type= str, required= True, help= "This field is must!")

    def get(self,username):
        book = BookModel.get_by_name(username)
        if bool:
            return book
        else:
            return {'message', 'book not found'}, 404

    def post(self):
        data = book.parser.parse_args()
        if BookModel.get_by_book_name(data['book_name']):
            return {'message':'book already exit'}, 400
        f = request.files['pdf']
        f2 = request.files['img']
        filename = datetime.utcnow().strftime('%Y_%m_%d_%H%M%S%f')[:-3]

        import requests
        img_url = ""
        pdf_url = ""
        if f2:
            url = 'http://burmesesoungs.com/mmnet/imgup.php?filename='+filename
            files = {'file': f2}
            response = requests.post(url, files=files)
            print(response.content)
            img_url = response.content.decode("utf-8")

        if f:
            url = 'http://burmesesoungs.com/mmnet/pdfup.php?filename='+filename
            files = {'file': f}
            response = requests.post(url, files=files)
            print(response.content)
            pdf_url = response.content.decode("utf-8")
        user_id = request.cookies.get('id')
        user_name = request.cookies.get('username')
        item = BookModel(int(user_id),user_name,data['book_name'],data['book_type'],pdf_url,img_url,data['author'],data['description'],"tags")
        try:
            item.save_to_db()
        except:
            return {'message': 'error occur while creating account'}, 500

        return item.json(), 201

    def delete(self, name):
        if BookModel.get_by_book_name(name) is None:
            return {'message','account doesn\'t exit'}, 404
        item = BookModel.get_by_book_name(name)
        item.delete_from_db()
        return {'message','book deleted'}, 200



class getbooks(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type= int, help= "This field is must!")

    def get(self):
        data = getbooks.parser.parse_args()
        pg_id = 1;
        if data["id"] is not None:
            pg_id = data["id"]
        books = BookModel.getbooklist(pg_id)
        next_c = pg_id + 1;
        book_items = books.items
        book_next = "null"
        print(books.has_next)
        if books.has_next:
            book_next = request.base_url + "?id=" + str(next_c)

        return jsonify(results=[i.json() for i in book_items],next=book_next)



class searchbooks(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type= int, help= "This field is must!")
    parser.add_argument('search', type=str, help= "This field is must!")


    def get(self):
        data = searchbooks.parser.parse_args()
        pg_id = 1;
        search_word = ""
        if data["id"] is not None:
            pg_id = data["id"]

        if data["search"] is not None:
            search_word = data["search"]

        books = BookModel.booksearch(page=pg_id,name=search_word)
        next_c = pg_id + 1;
        book_items = books.items
        book_next = "null"
        print(books.has_next)
        if books.has_next:
            book_next = request.base_url + "?id=" + str(next_c) + "&search=" + search_word

        return jsonify(results=[i.json() for i in book_items],next=book_next)


class filterbooks(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type= int, help= "This field is must!")
    parser.add_argument('filter', type=str, help= "This field is must!")


    def get(self):
        data = filterbooks.parser.parse_args()
        pg_id = 1;
        filter_word = ""
        if data["id"] is not None:
            pg_id = data["id"]

        if data["filter"] is not None:
            filter_word = data["filter"]

        books = BookModel.getbooksbyfilter(page=pg_id,filter_name=filter_word)
        next_c = pg_id + 1;
        book_items = books.items
        book_next = "null"
        print(books.has_next)
        if books.has_next:
            book_next = request.base_url + "?id=" + str(next_c) + "&filter=" + filter_word

        return jsonify(results=[i.json() for i in book_items],next=book_next)


#request contains
#     path             /page.html
#     script_root      /myapplication
#     base_url         http://www.example.com/myapplication/page.html
#     url              http://www.example.com/myapplication/page.html?x=y
#     url_root         http://www.example.com/myapplication/
