from flask import request
from flask_api import FlaskAPI, status, exceptions
from polling_system import PollingSystem
# curl -H "Content-Type: application/json" -X POST -d '{"title": "test", "vote": "test666"}' http://127.0.0.1:5000/addBlock

app = FlaskAPI(__name__)

@app.route("/vote/<poll_name>/<vote_for>", methods=['GET', 'POST'])
def vote(poll_name, vote_for):
    poll = PollingSystem.load_poll(poll_name)
    if poll.vote(vote_for):
        return {'created': True}, status.HTTP_201_CREATED, {'Access-Control-Allow-Origin': '*'}
    return {'created': False}, status.HTTP_406_NOT_ACCEPTABLE, {'Access-Control-Allow-Origin': '*'}


@app.route("/getResult/<poll_name>", methods=['GET'])
def get_poll_result(poll_name):
    poll = PollingSystem.load_poll(poll_name)
    return poll.get_poll_result(), status.HTTP_200_OK, {'Access-Control-Allow-Origin': '*'}

@app.route("/createPoll/<poll_name>", methods=['GET', 'POST'])
def create_poll(poll_name):
	pass
	

if __name__ == '__main__':
    app.run(debug=True)
