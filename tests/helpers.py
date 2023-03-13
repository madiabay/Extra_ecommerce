import json
from rest_framework_simplejwt import tokens


def access_token(user):
    return f'Bearer {tokens.AccessToken.for_user(user)}'


def load_json_data(path: str):
    with open(f'tests/data/{path}.json') as file:
        return json.load(file)