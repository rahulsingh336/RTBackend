import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import jwt_required

class Item(Resource):
    
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'item not found'}, 404


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        
        try:
            self.insert(item)
        except:
            return {"message": "An error occured insering the item"}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()     
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()     
        return {'message': 'items deleted'}

    def put(self, name):
        data = request.get_json()
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occured insering the item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured updating the item"}, 500
            #item = {'name': name, 'price': data['price']}
            #print(item)
            #item.update(data)
            #print(item)
            #print(data)
            #print(items)
        return item
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

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
        return {'items': items}