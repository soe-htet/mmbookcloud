from flask import Flask,request,render_template,redirect,url_for,send_from_directory,make_response
from flask_jwt import JWT
from flask_restful import Api
import os
from datetime import datetime

from security import authenticate,identity

from resources.post import sellpost,postList
from resources.member import Member,memberList,memberLogin
from resources.author import author,authorlist
from resources.booktype import booktype
from resources.book import book,getbooks,searchbooks,filterbooks
from models.authormodel import authormodel
from models.booktypemodel import booktypemodel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "soe"
api = Api(app)
jwt = JWT(app, authenticate, identity)
app.config['UPLOAD_FOLDER'] = 'imgs/'


# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(UserRegister,'/register')
# api.add_resource(ItemList,'/items')
# api.add_resource(Store, '/store/<string:name>')
# api.add_resource(StoreList,'/stores')

api.add_resource(sellpost,'/create-post')
api.add_resource(postList,'/get-posts')
api.add_resource(Member,'/register')
api.add_resource(memberLogin,'/login')
api.add_resource(memberList,'/get-members')
api.add_resource(author,'/add-author')
api.add_resource(booktype,'/add-type')
api.add_resource(book,'/add-book')
api.add_resource(getbooks,'/get-books')
api.add_resource(searchbooks,'/search-books')
api.add_resource(filterbooks,'/filter-books')


@app.route('/upload')
def upload_file1():
    username = request.cookies.get('username')
    if username == '':
        return redirect(url_for('login'))
    return render_template('bupload.html', data=[[x.json() for x in authormodel.query.all()],[x.json() for x in booktypemodel.query.all()]])


@app.route('/')
def index():
    username = request.cookies.get('username')
    resp = make_response(render_template("hello.html"))
    if username is not None:
        resp.set_cookie('username', username)
    else:
        resp.set_cookie('username','')
    return resp


@app.route('/login')
def login():
    if request.cookies.get('username') != '':
        return redirect(url_for('upload_file1'))
    return render_template('login.html')

@app.route('/uploadtest')
def uploadtest():
   return render_template('upload.html')

@app.route('/addauthor')
def add_author():
    if request.cookies.get('username') == '':
        return redirect(url_for('login'))
    return render_template('addauthor.html',data={'authors': [x.json() for x in authormodel.query.all()]})

@app.route('/addtype')
def add_type():
    if request.cookies.get('username') == '':
        return redirect(url_for('login'))
    return render_template('addtype.html',data={'authors': [x.json() for x in booktypemodel.query.all()]})



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['pdf']
      f2 = request.files['img']
      filename = datetime.utcnow().strftime('%Y_%m_%d_%H%M%S%f')[:-3]
      #tip = requests.post("http://burmesesoungs.com/mmnet/imgup.php",request.files['file'])
      #tip  = urllib2.urlopen("http://burmesesoungs.com/mmnet/imgup.php",request.files['file'])
      import requests
      url = 'http://burmesesoungs.com/mmnet/imgup.php?filename='+filename
      files = {'file': f2}
      response = requests.post(url, files=files)
      print(response.content)

      url = 'http://burmesesoungs.com/mmnet/pdfup.php?filename='+filename
      files = {'file': f}
      response = requests.post(url, files=files)
      print(response.content)

      f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
      return url_for('uploaded_file',
                                filename=f.filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/verify')
def verify():
    return render_template('verify.html')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001)

