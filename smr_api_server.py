import json

from flask import Flask, request, abort
from flask_cors import CORS

from smr_api.diary import Diary
from smr_api.exceptions import LoginFailedException

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
get = lambda route: app.route(route, methods=['GET'])
post = lambda route: app.route(route, methods=['POST'])
diary = None


@post('/auth')
def auth():
    global diary
    if 'username' in request.args and 'password' in request.args:
        try:
            diary = Diary(request.args['username'], request.args['password'])
        except LoginFailedException:
            return abort(401)
        return {'access_token': diary.token, 'user_id': diary.userId}
    else:
        return abort(400)


@get('/user')
def user():
    resp = Diary(token=request.headers['Access-Token'], user_id=request.headers['User-ID']).__dict__
    del resp['session'], resp['token']
    return resp


@get('/diary')
def day_diary():
    resp = Diary(token=request.headers['Access-Token'], user_id=request.headers['User-ID']).get_weeks()
    return resp


@get('/sample_diary')
def sample_diary():
    return json.load(open(__file__.replace('smr_api_server.py', 'sample_diary.json'), encoding='utf-8'))


if __name__ == '__main__':
    app.run()
