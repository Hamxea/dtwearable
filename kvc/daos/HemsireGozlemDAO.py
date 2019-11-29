from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.HemsireGozlem import HemsireGozlem


class HemsireGozlemDAO(AbstractDAO):

    def find_by_id(self, _id):
        return HemsireGozlem.query.filter_by(id=_id).first()

    def find_by_islem_id(self, islem_id):
        return HemsireGozlem.query.filter_by(islem_no=islem_id).first()