from ai.restful.daos.UserDAO import UserDAO
from ai.restful.models.User import User
from ai.restful.resources.security.AbstractUserResource import AbstractUserResource


class UserRegisterResource(AbstractUserResource):
    """ Kullanıcı kaydı oluşturan restful servis sınıfı"""

    userDAO = UserDAO()

    def post(self):
        """ Yeni kullanıcı kaydı oluşturan restful metodu """

        data = self._user_parser.parse_args()

        if self.userDAO.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = User(data['username'], data['password'])
        self.userDAO.save_to_db(user)

        return {"message": "User created successfully."}, 201
