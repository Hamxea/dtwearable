from keymind.daos.AbstractDAO import AbstractDAO
from keymind.models.User import User

"""
User nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
"""
class UserDAO(AbstractDAO):

    # username değerine göre User nesnesini veritabanından getiren metod
    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    # _id değerine göre User nesnesini veritabanından getiren metod
    def find_by_id(self, _id):
        return User.query.filter_by(id=_id).first()

