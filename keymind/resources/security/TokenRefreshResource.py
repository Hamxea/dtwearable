from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token

from keymind.resources.security.AbstractUserResource import AbstractUserResource


class TokenRefreshResource(AbstractUserResource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
