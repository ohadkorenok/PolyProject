from json import loads
from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from Task2.credentials import username, password, secret_key
import jwt
from datetime import datetime, timedelta
import hashlib
import os

app = Sanic("hello_example")


def generate_token(username_from_client: str) -> str:
    now_time = datetime.now()
    jwt_object = jwt.encode(
        {'iat': now_time, 'username': username_from_client, 'exp': now_time + timedelta(days=0, hours=12)},
        key=secret_key,
        algorithm='HS256')
    return jwt_object


def prepare_for_response(message, status_code):
    return json({"message": message, "status": status_code})


def validate_user(jwt_object: str):
    try:
        return jwt.decode(jwt_object.encode(), secret_key, algorithms='HS256')
    except Exception as e:
        return None


class SimpleView(HTTPMethodView):

    def post(self, request):
        """this method will be used to authenticate the user"""
        try:
            parameters = loads(request.body)
            username_from_client = parameters.get("username")
            if username_from_client == username and parameters.get('password') == password:
                jwt_token = generate_token(username_from_client).decode("utf-8")
            else:
                return prepare_for_response("No user or password related to that user have been found in the server",
                                            404)
        except Exception as e:
            return prepare_for_response("Server Error", 500)
        return prepare_for_response(jwt_token, 200)


def get_key(dict):
    """get the key that contains val"""
    a = [key for key, value in dict.items() if "val" in key.lower()][0]
    return a


class TaskBView(HTTPMethodView):
    def post(self, request):
        parameters = loads(request.body)
        token = request.headers['authorization']
        user = validate_user(token)

        if user is not None:
            return {dict["name"]: dict[[key for key, value in dict.items() if "val" in key.lower()][0]] for dict in
                    parameters}
        else:
            return prepare_for_response("Invalid token - please sign in", 403)


app.add_route(SimpleView.as_view(), '/login')
app.add_route(TaskBView.as_view(), '/taskb')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


def main(event, context):
    app.run(host="0.0.0.0", port=8000)
