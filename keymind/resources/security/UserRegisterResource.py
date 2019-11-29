from keymind.daos.UserDAO import UserDAO
from keymind.models.User import User
from keymind.resources.security.AbstractUserResource import AbstractUserResource


class UserRegisterResource(AbstractUserResource):
    userDAO = UserDAO()

    def post(self):
        data = self._user_parser.parse_args()

        if self.userDAO.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = User(data['username'], data['password'])
        self.userDAO.save_to_db(user)

        return {"message": "User created successfully."}, 201
