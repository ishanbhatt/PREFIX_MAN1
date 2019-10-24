import json
import os
import uuid

import requests

from flask import request, make_response, jsonify
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest, NotFound, Forbidden

from Prefix1_App import app, db
from Prefix1_App.models import User, Token

BACKEND = os.environ.get("BACKEND_URL", "http://localhost")


def get_uuid():
    return uuid.uuid4().hex


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    if users:
        return make_response({"USERS": [user.to_dict() for user in users]})
    else:
        raise NotFound("NO USERS YET")


@app.route("/tokens", methods=["GET"])
def get_tokens():
    tokens = Token.query.all()
    if tokens:
        return make_response({"TOKENS": [token.to_dict() for token in tokens]})
    else:
        raise NotFound("NO TOKENS YET")


@app.route("/create_user", methods=["POST"])
def add_user():
    request_dict = json.loads(request.data.decode("utf-8"))
    user = User(name=request_dict["name"], access_key=request_dict["access_key"])
    db.session.add(user)
    db.session.commit()
    return make_response(json.dumps({"Added": "OK"}), 201)


@app.route("/create_token", methods=["POST"])
def add_token():
    request_dict = json.loads(request.data.decode("utf-8"))

    try:
        user = User.query.filter_by(name=request_dict["name"], access_key=request_dict["access_key"]).one()
    except NoResultFound:
        raise Forbidden("User is invalid")

    token = Token(username=user.name, token=get_uuid())
    db.session.add(token)
    db.session.commit()
    return make_response(json.dumps({"Token": token.token}), 201)


# Will be called as /get_prefix?class=C
@app.route("/get_prefix", methods=["GET"])
def get_prefix():
    prefix_class = request.args.get("class")
    auth_header = request.headers.get("Authorization")
    request_token = auth_header.split(" ")[1]

    try:
        token = Token.query.filter_by(token=request_token).one()
    except NoResultFound:
        raise Forbidden("YOUR TOKEN IS INVALID, YOU CAN'T ASK FOR PREFIX")

    r = requests.get(f"{BACKEND}:6757/prefix?class={prefix_class}")
    if r.status_code == 200:
        return jsonify(r.json())
    else:
        return BadRequest("Could not parse the request")
