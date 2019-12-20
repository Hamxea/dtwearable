from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.LabSonucDTO import LabSonucDTO


class LabSonucDAO(AbstractDAO):
    """ LabSonuc nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir """

    def __init__(self):
        super().__init__(LabSonucDTO)

    def get_by_islem_no(self, islem_no: int):
        """ islem_no değerine göre LabSonuc nesnesini veritabanından getiren metod """

        return LabSonucDTO.query.filter_by(islem_no=islem_no).all()
