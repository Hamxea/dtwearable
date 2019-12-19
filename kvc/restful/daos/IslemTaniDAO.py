from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.IslemTaniDTO import IslemTaniDTO

class IslemTaniDAO(AbstractDAO):
    """
    Islem Tani nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def __init__(self):
        super().__init__(IslemTaniDTO)

    def find_by_id(self, _id:int) -> IslemTaniDTO:
        """ _id değerine göre IslemTani nesnesini veritabanından getiren metod """

        return IslemTaniDTO.query.filter_by(id=_id).first()

    def get_all_by_islem_no(self, islem_no:int):
        """ islem_no değerine göre IslemTani nesnelerini liste olarak veritabanından getiren metod """

        return IslemTaniDTO.query.filter_by(islem_no=islem_no).all()
