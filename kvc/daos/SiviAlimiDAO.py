from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.SiviAlimi import SiviAlimi


class SiviAlimiDAO(AbstractDAO):

    def find_by_id(self, _id):
        return SiviAlimi.query.filter_by(id=_id).first()

    # def find_by_islem_id(self, islem_id):
    #     return SiviAlimi.query.filter_by(islem_id=islem_id).all()