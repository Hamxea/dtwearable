from ai.restful.daos.AbstractDAO import AbstractDAO
from kvc.restful.models.IslemDTO import IslemDTO

class IslemDAO(AbstractDAO):
    """
    Islem nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def __init__(self):
        super().__init__(IslemDTO)

    def find_by_id(self, islem_no:int) -> IslemDTO:
        """
        Bu nesne için primary key id yerine islem_no olduğundan bu metod override edildi!!!
        islem_no değerine göre Islem nesnesini veritabanından getiren metod
        """

        return IslemDTO.query.filter_by(islem_no=islem_no).first()