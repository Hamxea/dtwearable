from flask_restful import Resource

from kvc.restful.daos.IslemTaniDAO import IslemTaniDAO

class IslemTaniResource(Resource):
    """
    Işlem Tani nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    islemTaniDAO = IslemTaniDAO()

    def get(self, islem_id: int):
        """ islem_id parametresine karsılık Islem Tani bilgisi donen metod """

        islemTani = self.islemTaniDAO.find_by_id(islem_id)
        if not islemTani:
            return {'message': 'Islem Tani Not Found'}, 404
        return islemTani.serialize, 200

    def delete(self, islem_id: int):
        """ islem_id parametresine göre Islem Tani nesnesini donen metod """

        islemTani = self.islemTaniDAO.find_by_id(islem_id)
        if not islemTani:
            return {'message': 'Islem Tani Not Found'}, 404
        self.islemTani.delete_from_db(islemTani)
        return {'message': 'Islem Tani deleted.'}, 200
