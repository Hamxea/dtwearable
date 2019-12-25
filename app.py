import logging
import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from ai.restful.resources.AIModelActivateResource import AIModelActivateResource
from ai.restful.resources.AIModelTrainerResource import AIModelTrainerResource
from ai.restful.resources.NotificationListResource import NotificationListResource
from ai.restful.resources.NotificationRegisterResource import NotificationRegisterResource
from ai.restful.resources.NotificationResource import NotificationResource
from ai.restful.resources.PredictionRegisterResource import PredictionRegisterResource
from ai.restful.resources.PredictionResource import PredictionResource
from ai.restful.resources.RuleViolationRegisterResource import RuleViolationRegisterResource
from ai.restful.resources.RuleViolationResource import RuleViolationResource
from ai.restful.resources.security.TokenRefreshResource import TokenRefreshResource
from ai.restful.resources.security.UserLoginResource import UserLoginResource
from ai.restful.resources.security.UserLogoutResource import UserLogoutResource
from ai.restful.resources.security.UserRegisterResource import UserRegisterResource
from ai.restful.resources.security.UserResource import UserResource
from ai.security.blacklist import BLACKLIST
from db import db
from kvc.restful.resources.HemsireGozlemRegisterResource import HemsireGozlemRegisterResource
from kvc.restful.resources.HemsireGozlemResource import HemsireGozlemResource
from kvc.restful.resources.IslemOperasyonRegisterResource import IslemOperasyonRegisterResource
from kvc.restful.resources.IslemOperasyonResource import IslemOperasyonResource
from kvc.restful.resources.IslemRegisterResource import IslemRegisterResource
from kvc.restful.resources.IslemResource import IslemResource
from kvc.restful.resources.IslemTaniRegisterResource import IslemTaniRegisterResource
from kvc.restful.resources.IslemTaniResource import IslemTaniResource
from kvc.restful.resources.LabSonucBatchRegisterResource import LabSonucBatchRegisterResource
from kvc.restful.resources.LabSonucRegisterResource import LabSonucRegisterResource
from kvc.restful.resources.LabSonucResource import LabSonucResource
from kvc.restful.resources.SiviAlimiRegisterResource import SiviAlimiRegisterResource
from kvc.restful.resources.SiviAlimiResource import SiviAlimiResource

app = Flask(__name__)
api = Api(app)

""" Gunicor ve app logging ayarları """
gunicorn_logger = logging.getLogger('gunicorn.debug')
app.logger.handlers = gunicorn_logger.handlers
# app.logger.setLevel(gunicorn_logger.level)
app.logger.setLevel(logging.INFO)

app.logger.debug("this is a DEBUG message for test")
app.logger.info("this is an INFO message for test")
app.logger.warning("this is a WARNING message for test")
app.logger.error("this is an ERROR message for test")
app.logger.critical("this is a CRITICAL message for test")

"""
SqlAlchemy ayarları
"""
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://arge05:arge05@10.0.0.59:5432/keymind')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(app)

# JWT configuration start
"""
JWT ayarları
"""
app.config[
    'JWT_SECRET_KEY'] = 'k@ym1nd'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    """
    JWT için identity olarak belirlenmiş User.id degerine gore kullanıcının
    admin bilgisini donen metod. Her istek öncesi bu metod çağırılır.
    """

    if identity == 1:  # TODO static id yerine veritabanından admin bilgisi alınmalı
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """ JWT için blackList özelliği aktif olduğun da token'ın blacklist'de bulunup bulunmadığı kontrol edilir """

    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    """ JWT için token süresi dolduğun da geri dönülecek mesajı üreten metod """

    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """ JWT için geçersiz token bulunması durumunda geri dönülecek mesajı üreten metod """

    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """ JWT için yetkisiz işlem yapılması durumunda geri dönülecek mesajı üreten metod """

    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """ JWT için token yenilemesi gerekmesi durumunda geri dönülecek mesajı üreten metod """

    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    """ JWT için iptal edilmiş token tespit edilmesi durumunda geri dönecek mesajı üreten metod """

    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


# JWT configuration ends

@app.before_first_request
def create_tables():
    """ Uygulamaya ilk istek geldiğinde tetiklenen ve gerekli veritabanı nesnelerini yaratan metod """

    db.create_all()


# Uygulamaya restful endpoint olarak tanımlanacak tüm sınıflar aşağıda belirtilir
# Keymind
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

# KVC resources
api.add_resource(IslemResource, '/kvc/islem/<int:islem_no>')
api.add_resource(IslemRegisterResource, '/kvc/islem')

api.add_resource(SiviAlimiResource, '/kvc/sivialimi/<int:sivi_alimi_id>')
api.add_resource(SiviAlimiRegisterResource, '/kvc/sivialimi')

api.add_resource(HemsireGozlemResource, '/kvc/hemsiregozlem/<int:hemsire_gozlem_id>')
api.add_resource(HemsireGozlemRegisterResource, '/kvc/hemsiregozlem')

api.add_resource(LabSonucResource, '/kvc/labsonuc/<int:lab_sonuc_id>')
api.add_resource(LabSonucRegisterResource, '/kvc/labsonuc')
api.add_resource(LabSonucBatchRegisterResource, '/kvc/labsonuc/batch')

api.add_resource(IslemTaniResource, '/kvc/islemtani/<int:id>')
api.add_resource(IslemTaniRegisterResource, '/kvc/islemtani')

api.add_resource(IslemOperasyonResource, '/kvc/islemoperasyon/<int:islem_operasyon_id>')
api.add_resource(IslemOperasyonRegisterResource, '/kvc/islemoperasyon')

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')