from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.SiviAlimiDTO import SiviAlimiDTO


class SiviAlimiDAO(AbstractDAO):
    """ Sıvı Alımı nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(SiviAlimiDTO)

        return SiviAlimiDTO.query.filter_by(id=_id).first()
