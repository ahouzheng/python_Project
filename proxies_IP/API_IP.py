'''
    API 接口
'''
from flask import Flask, jsonify, request

import db_Handler


app = Flask(__name__)


api_list = {
    'count': u'get the count of proxy',
    'get_one': u'get a random proxy',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route("/count/")
def count():
    return str(db_Handler.db_RowNum())


@app.route("/get_one/")
def get_one():
    row = db_Handler.db_GetOne()
    if len(row) == 0:
        return 'there is no proxies'
    else:
        return ':'.join(row)


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('ip')
    db_Handler.db_Delete(proxy)
    return 'Delete Successfully'


def API_Run():
    app.run(host='127.0.0.1', port=5000)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

