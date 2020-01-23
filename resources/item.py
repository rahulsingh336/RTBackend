import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        data = request.get_json()
        item = ItemModel(name, data['price'])
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured insering the item"}, 500

        return item.json(), 201
  
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'items deleted'}

    def put(self, name):
        data = request.get_json()
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                item = ItemModel(name, data['price'])
            except:
                return {"message": "An error occured insering the item"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occured updating the item"}, 500
            #item = {'name': name, 'price': data['price']}
            #print(item)
            #item.update(data)
            #print(item)
            #print(data)
            #print(items)
        item.save_to_db()
        return item.json()

class Itemlist(Resource):    
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]}) 

        connection.commit()
        connection.close()
        return {'items': [item.json() for item in ItemModel.query.all()]}