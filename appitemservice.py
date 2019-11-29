from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from user import UserRegister
from security import authenticate, identity
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = 'AR'
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})

items = []

jwt = JWT(app, authenticate, identity)   #/auth

class Item(Resource):
    
    @jwt_required()
    def get(self, name):
        #for item in items:
         #   if name == item['name']:
          #      return item
        #print(next(filter(lambda x: x['name'] == name, items), None))
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item }, 200 if item is not None else 404        

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": "An item with name {} already exists".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'items deleted'}

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            #item = {'name': name, 'price': data['price']}
            #print(item)
            item.update(data)
            #print(item)
            #print(data)
            #print(items)
        return item

class Itemlist(Resource):    
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')   # /student/Rolf
api.add_resource(Itemlist, '/items')
api.add_resource(UserRegister, '/register/<string:name>')

#app.run(host = '0.0.0.0', port = 5000, debug=True)
app.run(host = '0.0.0.0', port=os.environ.get('PORT'), debug=True)