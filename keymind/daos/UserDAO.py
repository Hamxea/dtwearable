from keymind.daos.AbstractDAO import AbstractDAO
from keymind.models.User import User


class UserDAO(AbstractDAO):

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def find_by_id(self, _id):
        return User.query.filter_by(id=_id).first()

