from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.Islem import Islem


class IslemDAO(AbstractDAO):

    def find_by_id(self, _id):
        return Islem.query.filter_by(id=_id).first()

    def find_by_islem_no(self, islem_no):
        return Islem.query.filter_by(islem_no=islem_no).first()