from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


voteFor = ['Trump', 'Bush', 'Merkel']


class MainPage(Resource):
    def get(self):
        return {'Title': 'Candidates for voting!',
                'Candidates': voteFor,
                }

api.add_resource(MainPage, '/')



if __name__ == '__main__':
    app.run(debug=True)