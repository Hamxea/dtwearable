from flask_jwt_extended import jwt_required#, get_raw_jwt

from ai.restful.resources.security.AbstractUserResource import AbstractUserResource
from ai.security.blacklist import BLACKLIST


class UserLogoutResource(AbstractUserResource):
    """ Class that logs the user out """

    @jwt_required
    def post(self):
        """ Method that blacklists the user's logout request token """

        #jti = get_raw_jwt()['jti']
        #BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
