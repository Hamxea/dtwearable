from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.IslemOperasyon import IslemOperasyon


class IslemOperasyonDAO(AbstractDAO):

    def find_by_id(self, _id):
        return IslemOperasyon.query.filter_by(id=_id).first()

    def find_by_islem_id(self, islem_id):
        return IslemOperasyon.query.filter_by(islem_id=islem_id).first()