from ai.restful.daos.UserDAO import UserDAO
from ai.restful.resources.security.AbstractUserResource import AbstractUserResource


class UserResource(AbstractUserResource):
    """ restful class that provides user information services """

    # TODO Buy methods need to be given admin privileges

    userDAO = UserDAO()

    def get(self, user_id: int):
        """ Method that returns user information based on user_id value """

        user = self.userDAO.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.serialize(), 200

    def delete(self, user_id: int):
        """ Method that deletes user based on user_id value """
        
        user = self.userDAO.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        self.userDAO.delete_from_db(user)
        return {'message': 'User deleted.'}, 200
