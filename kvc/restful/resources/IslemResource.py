from flask_restful import Resource

from kvc.restful.daos.IslemDAO import IslemDAO

class IslemResource(Resource):
    """
    Islem nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    islemDAO = IslemDAO()

    def get(self, islem_id: int):
        """ islem_id parametresine karsılık Islem bilgisi donen metod """

        islem = self.islemDAO.find_by_id(islem_id)
        if not islem:
            return {'message': 'Islem Not Found'}, 404
        return islem.serialize, 200

    def delete(self, islem_id: int):
        """ islem_id parametresine göre Islem nesnesini donen metod """

        islem = self.islemDAO.find_by_id(islem_id)
        if not islem:
            return {'message': 'Islem Not Found'}, 404
        self.islemDAO.delete_from_db(islem)
        return {'message': 'Islem deleted.'}, 200