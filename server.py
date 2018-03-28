from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
# from blockchain import BlockChain

app = Flask(__name__)


# b = BlockChain()

@app.route('/')
def index():
    # if request.method == 'POST':
    #     text = request.form['text']
    #     if len(text) < 1:
    #         return redirect(url_for('index'))
    #         make_proof = False
    #     b.add_block(title=text)
    #     return redirect(url_for('index'))
    return render_template('index.html')

# @app.route('/check', methods=[ 'POST'])
# def integrity():
#     results = b.check_blocks_integrity()
#     if request.method == 'POST':
#         return render_template('index.html', results=results)
#     return render_template('index.html')

# @app.route('/mining', methods=[ 'POST'])
# def mining():
#     if request.method == 'POST':
#         max_index = int(blockChain.get_next_block())

#         for i in range(2, max_index):
#             blockChain.get_POW(i)
#         return render_template('index.html', querry=max_index)
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)