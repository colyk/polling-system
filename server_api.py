from flask import request
from flask import Flask, url_for
import blockchain
#curl -H "Content-Type: application/json" -X POST -d '{"title": "test", "vote": "test666"}' http://127.0.0.1:5000/addBlock

app = Flask(__name__)

bc = blockchain.BlockChain()

@app.route("/getBlocks", methods=['GET'])
def getBlocks():
    #resp = flask.make_response(bc.get_current_blocks(), 200)
    #resp.headers.extend({'Access-Control-Allow-Origin': '*'})
    return bc.get_current_blocks(), status.HTTP_200_OK, {'Access-Control-Allow-Origin': '*'}


@app.route("/check", methods=['GET'])
def checkInt():
    return bc.check_blocks_integrity(), status.HTTP_200_OK, {'Access-Control-Allow-Origin': '*'}


@app.route("/addBlock", methods=['POST'])
def addBlock():
    title = str(request.data.get('title'))
    vote = str(request.data.get('vote'))
    print(title)
    print(vote)
    bc.add_block(title=title, vote_for=vote)
    return {'vote': vote, 'title': title}, status.HTTP_201_CREATED, {'Access-Control-Allow-Origin': '*'}


if __name__ == '__main__':
    app.run(debug=False)
