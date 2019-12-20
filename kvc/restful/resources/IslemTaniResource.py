from flask_restful import Resource

from kvc.restful.daos.IslemTaniDAO import IslemTaniDAO

class IslemTaniResource(Resource):
    """
    Işlem Tani nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    islem_tani_DAO = IslemTaniDAO()

    def get(self, id: int):
        """ id parametresine karsılık Islem Tani bilgisi donen metod """

        islem_tani = self.islem_tani_DAO.find_by_id(id)
        if not islem_tani:
            return {'message': 'Islem Tani Not Found'}, 404
        return islem_tani.serialize, 200

    def delete(self, id: int):
        """ id parametresine göre Islem Tani nesnesini donen metod """

        islem_tani = self.islem_tani_DAO.find_by_id(id)
        if not islem_tani:
            return {'message': 'Islem Tani Not Found'}, 404
        self.islem_tani_DAO.delete_from_db(islem_tani)
        return {'message': 'Islem Tani deleted.'}, 200


