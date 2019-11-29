from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp

from keymind.daos.UserDAO import UserDAO
from keymind.resources.security.AbstractUserResource import AbstractUserResource


class UserLoginResource(AbstractUserResource):
    userDAO = UserDAO()

    def post(self):
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
