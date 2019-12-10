from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token

from ai.restful.resources.security.AbstractUserResource import AbstractUserResource


class TokenRefreshResource(AbstractUserResource):
    """ Belirli durumlarda Token değerinin yeniden üretilmesini sağlayan sınıf """

    @jwt_refresh_token_required
    def post(self):
        """ Yeni token değerini oluşturan metod """

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
