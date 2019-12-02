from keymind.daos.UserDAO import UserDAO
from keymind.resources.security.AbstractUserResource import AbstractUserResource


class UserResource(AbstractUserResource):
    # TODO Buy metodlara admin yetkisi verilmesi gerekiyor

    userDAO = UserDAO()

    def get(self, user_id: int):
        user = self.userDAO.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    def delete(self, user_id: int):
        user = self.userDAO.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        self.userDAO.delete_from_db(user)
        return {'message': 'User deleted.'}, 200