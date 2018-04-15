from flask import request
from flask_api import FlaskAPI, status
from polling_system import PollingSystem

# curl -H "Content-Type: application/json" -X POST -d '{"poll_name": "test123", "description": "test666"}' http://127.0.0.1:5000/createPoll/
# requests.post('http://127.0.0.1:5000/createPoll/', json={'poll_name':'kek', "description": 'fdsdfs', 'options': ['lol', 'kek']})
app = FlaskAPI(__name__)


HEADER = {'Access-Control-Allow-Origin': '*'}


@app.route("/addVote/", methods=['GET', 'POST'])
def vote():
    response = request.get_json(force=True)
    try:
        poll_name = response['poll_name']
    except Exception:
        return {'code': '400', 'msg': 'json must insist poll_name key'}, status.HTTP_400_BAD_REQUEST, HEADER

    try:
        vote_for = response['vote_for']
    except Exception:
        return {'code': '400', 'msg': 'json must insist vote_for key'}, status.HTTP_400_BAD_REQUEST, HEADER

    if poll_name not in PollingSystem.get_active_polls()['polls']:
        return {'code': '500', 'msg': 'poll with poll_name: %s has not been created yet' % poll_name}, status.HTTP_500_INTERNAL_SERVER_ERROR, HEADER

    poll = PollingSystem.load_poll(poll_name)
    if poll.vote(vote_for):
        return {'code': '201'}, status.HTTP_201_CREATED, HEADER
    return {'code': '500', 'msg': 'vote_for: %s is not in polling options' % vote_for}, status.HTTP_500_INTERNAL_SERVER_ERROR, HEADER


@app.route("/getResult/", methods=['GET', 'POST'])
def get_poll_result():
    response = request.get_json(force=True)
    try:
        poll_name = response['poll_name']
    except Exception:
        return {'code': '400', 'msg': 'json must insist poll_name key'}, status.HTTP_400_BAD_REQUEST, HEADER

    if poll_name not in PollingSystem.get_active_polls()['polls']:
        return {'code': '500', 'msg': 'poll with poll_name: %s has not been created yet' % poll_name}, status.HTTP_500_INTERNAL_SERVER_ERROR, HEADER

    poll = PollingSystem.load_poll(poll_name)
    return poll.get_poll_result(), status.HTTP_200_OK, HEADER


@app.route("/createPoll/", methods=['GET', 'POST'])
def create_poll():
    termination_time = 0
    response = request.get_json(force=True)
    try:
        poll_name = response['poll_name']
    except Exception:
        return {'code': '400', 'msg': 'json must insist poll_name key'}, status.HTTP_400_BAD_REQUEST, HEADER

    try:
        description = response['description']
    except Exception:
        return {'code': '400', 'msg': 'json must insist poll_name description'}, status.HTTP_400_BAD_REQUEST, HEADER

    try:
        options = response['options']
    except Exception:
        return {'code': '400', 'msg': 'json must insist options: [] key'}, status.HTTP_400_BAD_REQUEST, HEADER

    try:
        termination_time = response['termination_time']
    except Exception:
        pass

    if poll_name in PollingSystem.get_active_polls()['polls']:
        return {'code': '500', 'msg': 'poll with poll_name: %s has been created already' % poll_name}, status.HTTP_500_INTERNAL_SERVER_ERROR, HEADER

    PollingSystem.add_poll(
        poll_name=poll_name, description=description, options=options, termination_time=termination_time)
    return {'code': '201'}, status.HTTP_201_CREATED, HEADER


@app.route("/getActivePolls/", methods=['GET'])
def get_active_polls():
    return PollingSystem.get_active_polls(), status.HTTP_200_OK, HEADER


@app.route("/getPollInfo/", methods=['GET', 'POST'])
def get_info():
    response = request.get_json(force=True)
    try:
        poll_name = response['poll_name']
    except Exception:
        return {'code': '400', 'msg': 'json must insist poll_name key'}, status.HTTP_400_BAD_REQUEST, HEADER

    if poll_name not in PollingSystem.get_active_polls()['polls']:
        return {'code': '500', 'msg': 'poll with poll_name: %s has not been created yet' % poll_name}, status.HTTP_500_INTERNAL_SERVER_ERROR, HEADER

    poll = PollingSystem.load_poll(poll_name)
    return poll.get_info(), status.HTTP_200_OK, HEADER


@app.route("/zipPoll/", methods=['GET', 'POST'])
def zip_poll():
    response = request.get_json(force=True)
    try:
        poll_name = response['poll_name']
    except Exception:
        return {'code': '400', 'msg': 'json must insist poll_name key'}, status.HTTP_400_BAD_REQUEST, HEADER

    if poll_name not in PollingSystem.get_active_polls()['polls']:
        return {'code': '500', 'msg': 'poll with poll_name: %s has not been created yet' % poll_name}, status.HTTP_500_INTERNAL_SERVER_ERROR, HEADER

    poll = PollingSystem.load_poll(poll_name)
    poll.zip_poll()
    return {'code': '200'}, status.HTTP_200_OK, HEADER


@app.route("/getArchivedPolls/", methods=['GET'])
def get_archived_polls():
    return {'polls': PollingSystem.get_archived_polls()}, status.HTTP_200_OK, HEADER


if __name__ == '__main__':
    app.run(debug=True)
