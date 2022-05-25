from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp

from ai.restful.daos.UserDAO import UserDAO
from ai.restful.resources.security.AbstractUserResource import AbstractUserResource


class UserLoginResource(AbstractUserResource):
    """ Rest service class that allows the user to login and generates Tokens for later use """

    userDAO = UserDAO()

    def post(self):
        """ User login class returns Token value """

        data = self._user_parser.parse_args()

        user = self.userDAO.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401
