from keymind.daos.AbstractDAO import AbstractDAO
from kvc.models.SiviAlimi import SiviAlimi


class SiviAlimiDAO(AbstractDAO):
    """ Sıvı Alımı nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def find_by_id(self, _id):
        """ _id değerine göre Sıvı Alımı nesnesini veritabanından getiren metod """

        return SiviAlimi.query.filter_by(id=_id).first()
