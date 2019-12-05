from keymind.daos.AbstractDAO import AbstractDAO
from keymind.models.User import User

class UserDAO(AbstractDAO):
    """
    User nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def find_by_username(self, username):
        """ username değerine göre User nesnesini veritabanından getiren metod """

        return User.query.filter_by(username=username).first()

    def find_by_id(self, _id):
        """ _id değerine göre User nesnesini veritabanından getiren metod """

        return User.query.filter_by(id=_id).first()

