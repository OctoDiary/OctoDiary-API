from smr_api.diary import Diary
from smr_api.exceptions import LoginFailedException

from flask import Flask, request, abort


app = Flask(__name__)
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


if __name__ == '__main__':
    app.run()
