from ai.restful.daos.UserDAO import UserDAO
from ai.restful.models.UserDTO import UserDTO
from ai.restful.resources.security.AbstractUserResource import AbstractUserResource


class UserRegisterResource(AbstractUserResource):
    """ Restful service class that creates user registration """

    userDAO = UserDAO()

    def post(self):
        """ Restful method that creates a new user record """

        data = self._user_parser.parse_args()

        if self.userDAO.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserDTO(data['username'], data['password'])
        self.userDAO.save_to_db(user)

        return {"message": "User created successfully."}, 201
