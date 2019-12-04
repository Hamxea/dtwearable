import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from keymind.security.blacklist import BLACKLIST
from db import db

from keymind.resources.security.UserLoginResource import UserLoginResource
from keymind.resources.security.UserResource import UserResource
from keymind.resources.security.TokenRefreshResource import TokenRefreshResource
from keymind.resources.security.UserLogoutResource import UserLogoutResource
from keymind.resources.security.UserRegisterResource import UserRegisterResource

from kvc.resources.IslemRegisterResource import IslemRegisterResource
from kvc.resources.IslemResource import IslemResource

app = Flask(__name__)
api = Api(app)

"""
SqlAlchemy ayarları
"""
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://arge05:arge05@10.0.0.59:5432/keymind')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(app)

# JWT configuration start
"""
JWT ayarları
"""
app.config['JWT_SECRET_KEY'] = 'k@ym1nd'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)

"""
JWT için identity olarak belirlenmiş User.id degerine gore kullanıcının
admin bilgisini donen metod. Her istek öncesi bu metod çağırılır.
"""
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # TODO static id yerine veritabanından admin bilgisi alınmalı
        return {'is_admin': True}
    return {'is_admin': False}


"""
JWT için blackList özelliği aktif olduğun da token'ın blacklist'de bulunup bulunmadığı kontrol edilir
"""
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


"""
JWT için token süresi dolduğun da geri dönülecek mesajı üreten metod
"""
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401

"""
JWT için geçersiz token bulunması durumunda geri dönülecek mesajı üreten metod
"""
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

"""
JWT için yetkisiz işlem yapılması durumunda geri dönülecek mesajı üreten metod
"""
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

"""
JWT için token yenilemesi gerekmesi durumunda geri dönülecek mesajı üreten metod
"""
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401

"""
JWT için iptal edilmiş token tespit edilmesi durumunda geri dönecek mesajı üreten metod 
"""
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401
# JWT configuration ends

"""
Uygulamaya ilk istek geldiğinde tetiklenen ve gerekli veritabanı nesnelerini yaratan metod 
"""
@app.before_first_request
def create_tables():
    db.create_all()

# Uygulamaya restful endpoint olarak tanımlanacak tüm sınıflar aşağıda belirtilir
# Security resources
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(TokenRefreshResource, '/refresh')
api.add_resource(UserLogoutResource, '/logout')

# KVK resources
api.add_resource(IslemResource, '/islem/<int:islem_id>')
api.add_resource(IslemRegisterResource, '/islem')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
