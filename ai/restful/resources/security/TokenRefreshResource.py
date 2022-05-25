from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token #jwt_refresh_token_required

from ai.restful.resources.security.AbstractUserResource import AbstractUserResource


class TokenRefreshResource(AbstractUserResource):
    """ Class that enables Token value reproduction in certain situations """

    @jwt_required
    def post(self):
        """ Yeni token değerini oluşturan metod """

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
