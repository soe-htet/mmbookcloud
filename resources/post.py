from flask_restful import Resource, reqparse
from models.post import postModel

class sellpost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type= int, required= True, help= "This field is must!")
    parser.add_argument('noofkg', type= int, required= True, help= "This field is must!")
    parser.add_argument('priceperkg', type= str, required= True, help= "This field is must!")
    parser.add_argument('ava_date', type= int, required= True, help= "This field is must!")
    parser.add_argument('desc', type= str, required= True, help= "This field is must!")
    parser.add_argument('_from', type= str, required= True, help= "This field is must!")
    parser.add_argument('_to', type= str, required= True, help= "This field is must!")
    parser.add_argument('status', type= str, required= True, help= "This field is must!")

    def get(self, user_id):
        posts = postModel.get_by_user_id(user_id)
        if posts:
            return posts
        else:
            return {'message', 'no post found'}, 404

    def post(self):
        data = sellpost.parser.parse_args()
        post = postModel(data['user_id'],data['noofkg'],data['priceperkg'],data['ava_date'],data['desc'],data['_from'],data['_to'],data['status'])
        try:
            post.save_to_db()
        except:
            return {'message': 'error occur while creating post'}, 500

        return {'message': 'post successfully created'}, 201

    def delete(self, post_id):
        if postModel.get_by_post_id(post_id) is None:
            return {'message','post doesn\'t exit'}, 404
        post = postModel.get_by_post_id(post_id)
        post.delete_from_db()
        return {'message','post deleted'}, 200


class postList(Resource):
    def get(self):
        return {'posts': [x.json() for x in postModel.query.all()]}
