import requests
from smr_api.exceptions import *
from smr_api.constants import *


class Diary:
    def __init__(self, login: str = None, password: str = None, token: str = None, user_id: str = None):
        self.session = requests.Session()
        if login and password:
            self.session.headers['Access-Token'] = self.token_get(login, password)
        if token:
            self.session.headers['Access-Token'] = token
            self.userId = int(user_id)
        if login and password and token:
            raise TooManyCredentialsGivenException
        elif (not login) and (not password) and (not token):
            raise NoCredentialsGivenException
        elif (login and not password) or (password and not login):
            raise NotEnoughCredentialsException
        self.token = self.session.headers['Access-Token']
        me = self.get_me_user()['contextPersons'][0]
        self.avatarUrl = me['avatarUrl']
        self.userId = me['userId']
        self.personId = me['personId']
        self.sex = me['sex']
        self.firstName = me['firstName']
        self.lastName = me['lastName']
        self.middleName = me['middleName']
        school = me['school']
        self.schoolId = school['id']
        self.schoolName = school['name']
        self.schoolGeoPosition = (school['latitude'], school['longitude'])
        self.schoolAvatarUrl = school['avatarUrl']
        group = me['group']
        self.groupId = group['id']
        self.className = group['name']
        self.classLetter = group['name'][-1]
        self.classNumber = int(group['name'][:-1])
        rating = self.get_rating()
        self.rankingPlace = rating['history']['rankingPosition']['place']
        self.rankingHistory = rating['history']['historyItems']

    def token_get(self, login: str, password: str) -> str:
        response = self.session.post(AUTH_URL, json={
            'clientId': CLIENT_ID,
            'clientSecret': CLIENT_SECRET,
            'scope': ALL_SCOPE,
            'username': login,
            'password': password
        })
        if 'type' in response.json() and response.json()['type'] == 'authorizationFailed':
            raise LoginFailedException
        if response.status_code > 299 or 'accessToken' not in response.json()['credentials']:
            raise ServerException
        self.userId = str(response.json()['credentials']['userId'])
        return response.json()['credentials']['accessToken']

    def custom_url(self, url: str = None, params: dict = None, method: str = None, rest_method: str = 'GET'):
        if params is None:
            params = {}
        if url or method and not (url and method):
            if url:
                return self.session.request(rest_method, url, params)
            if method:
                return self.session.request(rest_method, BASE_URL + method, params)
        else:
            raise InvalidRequestException

    def get_me_user(self) -> dict:
        return self.session.\
            get(BASE_URL + 'users/' + str(self.userId) + '/context').json()

    def get_rating(self) -> dict:
        return self.session.\
            get(BASE_URL + 'persons/' + str(self.personId) + '/groups/' + str(self.groupId) + '/rating').json()
