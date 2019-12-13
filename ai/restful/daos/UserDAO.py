from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.UserDTO import UserDTO

class UserDAO(AbstractDAO):
    """
    User nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def __init__(self):
        super().__init__(UserDTO)

    def find_by_username(self, username):
        """ username değerine göre User nesnesini veritabanından getiren metod """

        return UserDTO.query.filter_by(username=username).first()

