from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'body': 'Hello world!'}

class Lol(Resource):
    def get(self):
        return {'body': 'Lol'}

api.add_resource(HelloWorld, '/')
api.add_resource(Lol, '/lol')

if __name__ == '__main__':
    app.run(debug=True)