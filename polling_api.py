from flask import request, jsonify
from flask_api import FlaskAPI, status, exceptions
from polling_system import PollingSystem
from flask_cors import CORS
# curl -H "Content-Type: application/json" -X POST -d '{"title": "test", "vote": "test666"}' http://127.0.0.1:5000/addBlock
# requests.post('http://127.0.0.1:5000/createPoll/', json={'poll_name':'kek', "description": 'fdsdfs', 'options': ['lol', 'kek']})
app = FlaskAPI(__name__)
CORS(app)

# created = {'created': True}
# not_created = {'created': False}


@app.route("/addVote/", methods=['GET', 'POST'])
def vote():
    try:
        poll_name = request.get_json()['poll_name']
        vote_for = request.get_json()['vote_for']
    except Exception:
        return {'created': False}, status.HTTP_406_NOT_ACCEPTABLE, {'Access-Control-Allow-Origin': '*'}
    poll = PollingSystem.load_poll(poll_name)
    if poll.vote(vote_for):
        return {'created': True}, status.HTTP_201_CREATED, {'Access-Control-Allow-Origin': '*'}
    return {'created': False}, status.HTTP_406_NOT_ACCEPTABLE, {'Access-Control-Allow-Origin': '*'}


@app.route("/getResult/", methods=['GET', 'POST'])
def get_poll_result():
    try:
        poll_name = request.get_json()['poll_name']
    except Exception:
        return {'created': False}, status.HTTP_406_NOT_ACCEPTABLE, {'Access-Control-Allow-Origin': '*'}
    poll = PollingSystem.load_poll(poll_name)
    return poll.get_poll_result(), status.HTTP_200_OK, {'Access-Control-Allow-Origin': '*'}


@app.route("/createPoll/", methods=['GET', 'POST'])
def create_poll():
    print(request.get_json())
    try:
        poll_name = request.get_json()['poll_name']
        description = request.get_json()['description']
        options = request.get_json()['options']
    except Exception:
        return {'created': False}, status.HTTP_406_NOT_ACCEPTABLE, {'Access-Control-Allow-Origin': '*'}
    PollingSystem.add_poll(
        poll_name=poll_name, description=description, options=options)
    return {'created': True}, status.HTTP_201_CREATED, {'Access-Control-Allow-Origin': '*'}


@app.route("/getActivePolls/", methods=['GET'])
def get_active_polls():
    return PollingSystem.get_active_polls(), status.HTTP_200_OK, {'Access-Control-Allow-Origin': '*'}


@app.route("/getPollInfo/", methods=['GET', 'POST'])
def get_info():
    try:
        poll_name = request.get_json()['poll_name']
    except Exception:
        return {'created': False}, status.HTTP_406_NOT_ACCEPTABLE, {'Access-Control-Allow-Origin': '*'}
    poll = PollingSystem.load_poll(poll_name)
    return poll.get_info(), status.HTTP_200_OK, {'Access-Control-Allow-Origin': '*'}


if __name__ == '__main__':
    app.run(debug=True)
