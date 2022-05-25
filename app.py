import logging
import os
import random

from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_socketio import SocketIO, emit, join_room, send
from flask_cors import CORS

from ai.restful.resources.AIModelActivateResource import AIModelActivateResource
from ai.restful.resources.AIModelTrainerResource import AIModelTrainerResource
from ai.restful.resources.NotificationListResource import NotificationListResource
from ai.restful.resources.NotificationRegisterResource import NotificationRegisterResource
from ai.restful.resources.NotificationResource import NotificationResource
from ai.restful.resources.PredictionRegisterResource import PredictionRegisterResource
from ai.restful.resources.PredictionResource import PredictionResource
from ai.restful.resources.RuleViolationRegisterResource import RuleViolationRegisterResource
from ai.restful.resources.RuleViolationResource import RuleViolationResource
from ai.restful.resources.StatisticsResource import StatisticsResource
from ai.restful.resources.security.TokenRefreshResource import TokenRefreshResource
from ai.restful.resources.security.UserLoginResource import UserLoginResource
from ai.restful.resources.security.UserLogoutResource import UserLogoutResource
from ai.restful.resources.security.UserRegisterResource import UserRegisterResource
from ai.restful.resources.security.UserResource import UserResource
from ai.security.blacklist import BLACKLIST
from db import db

from utils_test import blood_pressure_test

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*', cors_credentials=True)

""" Gunicorn and app logging settings """
gunicorn_logger = logging.getLogger('gunicorn.debug')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG)

app.logger.debug("this is a DEBUG message for test")
app.logger.info("this is an INFO message for test")
app.logger.warning("this is a WARNING message for test")
app.logger.error("this is an ERROR message for test")
app.logger.critical("this is a CRITICAL message for test")

"""
SqlAlchemy settings
"""
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://postgres:postgres@localhost:5432/dtwearable')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(app)

# JWT configuration start
"""
JWT configuration
"""
app.config[
    'JWT_SECRET_KEY'] = 'k@ym1nd'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)

socket_clients = []


@app.route('/', methods=['GET', 'POST'])
def page():
    return "<h1 style='color: red;'>DT Wearable!</h1>"


@app.route('/home', methods=['GET', 'POST'])
def home():
    return "<h1 style='color: red;'>DT Wearable!</h1>"


@app.route('/ai/prediction/test', methods=['GET', 'POST'])
def prediction_test():

    result = random.choice(blood_pressure_test)
    return jsonify(result,
                   {'systolic_pressure': result[0],
                    'diastolic_pressure': result[1]}
                   )


@socketio.on('connect')
def connected():
    print(request.namespace)
    print(request.sid)
    socket_clients.append(request.namespace)
    print("ok")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected....')
    print(request.namespace)
    # socket_clients.remove(request.sid)


@jwt._user_claims_callback
def add_claims_to_jwt(identity):
    """
    According to the User.id value determined as identity for JWT, the user
     The method that returns the admin information. This method is called before every request.
    """

    if identity == 1:  # TODO static id yerine veritabanından admin bilgisi alınmalı
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader # token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """ When the blackList feature for JWT is active, it is checked whether the token is in the blacklist. """

    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    """ Method that generates the message to be returned when the token expires for JWT """

    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """ Method that generates message to return if invalid token is found for JWT """

    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """ The method that generates the message to be returned in case of unauthorized operation for the JWT """

    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """ Method that generates the message to return if JWT requires token renewal """

    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    """ Method that generates the message to return if revoked token is detected for JWT """

    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


# JWT configuration ends

@app.before_first_request
def create_tables():
    """ The method that is triggered when the application receives the first request and creates the required database objects """

    db.create_all()


# socket bildirim

@socketio.on('messag<e')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


# All classes that will be defined as restful endpoints to the application are specified below
# dtwearable
# Security resources
api.add_resource(UserRegisterResource, '/ai/security/register')
api.add_resource(UserLoginResource, '/ai/security/login')
api.add_resource(UserResource, '/ai/security/user/<int:user_id>')
api.add_resource(TokenRefreshResource, '/ai/security/refresh')
api.add_resource(UserLogoutResource, '/ai/security/logout')

# AI
api.add_resource(RuleViolationResource, '/ai/ruleviolation/<int:rule_violation_id>')
api.add_resource(RuleViolationRegisterResource, '/ai/ruleviolation')

api.add_resource(AIModelTrainerResource, '/ai/trainmodel')
api.add_resource(AIModelActivateResource, '/ai/activatemodel')

api.add_resource(PredictionRegisterResource, '/ai/prediction')
api.add_resource(PredictionResource, '/ai/prediction/<int:prediction_id>')

api.add_resource(NotificationResource, '/ai/notification/<int:notification_id>')
api.add_resource(NotificationRegisterResource, '/ai/notification')
api.add_resource(NotificationListResource, '/ai/notification/list')

api.add_resource(StatisticsResource, '/ai/statistics')

# DT resources


db.init_app(app)

if __name__ == '__main__':
    # app.run(port=5000, debug=True, host='0.0.0.0')
    socketio.run(app, host='0.0.0.0', port=5005, debug=True)