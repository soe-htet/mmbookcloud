
from flask_restful import Resource,reqparse
import sqlite3
from models.item import ItemModel
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type= float, required= True, help= "This field is must!")
    parser.add_argument('store_id', type= int, required= True, help= "This field is must!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}


    def post(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            return {'message': "An item with name '{}' is already exit".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'error occur while inserting'}, 500
        return item.json(), 201


    def delete(self,name):
        item = ItemModel.get_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message': 'item not found'}

        return {"message": "item deleted"}

    def put(self,name):
        item = ItemModel.get_by_name(name)
        data = Item.parser.parse_args()

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
