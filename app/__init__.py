# app/__init__.py
import json
import os
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response

# local import

from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import Resttesting, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    bcrypt = Bcrypt(app)
   # config_name = os.getenv('app_config', 'DEVELOPMENT')
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/resttest1/', methods=['POST', 'GET'])
    def resttest1():
        # get the access token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authed
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        resttesting = Resttesting(name=name, created_by=user_id)
                        resttesting.save()
                        response = jsonify({
                            'paragraph': resttesting.paragraph,
                            'label': resttesting.label,
                            'textbox':resttesting.textbox,
                            'checkbox':resttesting.checkbox,
                            'radiobutton':resttesting.radiobutton,
                            'dropdown':resttesting.dropdown,
                            'rating':resttesting.rating,
                            'switch':resttesting.switch,
                            'date':resttesting.date,
                            'userid': resttesting.id,
                            'name': resttesting.name,
                            'date_created': resttesting.date_created,
                            'date_modified': resttesting.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET
                    # get all the restest1 for this user
                    resttest1 = Resttesting.get_all(user_id)
                    results = []

                    for resttesting in resttest1:
                        obj = {
                            'id': resttesting.id,
                            'name': resttesting.name,
                            'paragraph': resttesting.paragraph,
                            'label': resttesting.label,
                            'textbox':resttesting.textbox,
                            'checkbox':resttesting.checkbox,
                            'radiobutton':resttesting.radiobutton,
                            'dropdown':resttesting.dropdown,
                            'rating':resttesting.rating,
                            'switch':resttesting.switch,
                            'date':resttesting.date,
                            'date_created': resttesting.date_created,
                            'date_modified': resttesting.date_modified,
                            'created_by': user_id
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/resttest1/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def resttesting_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                resttesting = Resttesting.query.filter_by(id=id).first()
                if not resttesting:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    resttesting.delete()
                    return {
                        "message": "resttesting {} deleted".format(resttesting.id)
                    }, 200
                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    resttesting.name = name
                    resttesting.save()
                    response = {
                          'paragraph': resttesting.paragraph,
                            'label': resttesting.label,
                            'textbox':resttesting.textbox,
                            'checkbox':resttesting.checkbox,
                            'radiobutton':resttesting.radiobutton,
                            'dropdown':resttesting.dropdown,
                            'rating':resttesting.rating,
                            'switch':resttesting.switch,
                            'date':resttesting.date,
                            'userid': resttesting.id,
                            'name': resttesting.name,
                            'date_created': resttesting.date_created,
                            'date_modified': resttesting.date_modified,
                            'created_by': user_id
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # GET
                    response = jsonify({
                          'paragraph': resttesting.paragraph,
                            'label': resttesting.label,
                            'textbox':resttesting.textbox,
                            'checkbox':resttesting.checkbox,
                            'radiobutton':resttesting.radiobutton,
                            'dropdown':resttesting.dropdown,
                            'rating':resttesting.rating,
                            'switch':resttesting.switch,
                            'date':resttesting.date,
                            'userid': resttesting.id,
                            'name': resttesting.name,
                            'date_created': resttesting.date_created,
                            'date_modified': resttesting.date_modified,
                            'created_by': user_id
                    })
                    return make_response(response), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app