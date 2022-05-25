from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.UserDTO import UserDTO

class UserDAO(AbstractDAO):
    """
    Contains the methods by which database operations are performed for the User object
    """

    def __init__(self):
        super().__init__(UserDTO)

    def find_by_username(self, username):
        """ Method fetching User object from database based on username value """

        return UserDTO.query.filter_by(username=username).first()

