from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.LabSonucDTO import LabSonucDTO


class LabSonucDAO(AbstractDAO):
    """ LabSonuc nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(LabSonucDTO)

    def get_by_islem_id(self, islem_id: int):
        """ islem_no değerine göre LabSonuc nesnesini veritabanından getiren metod """

        return LabSonucDTO.query.filter_by(islem_id=islem_id).all()
