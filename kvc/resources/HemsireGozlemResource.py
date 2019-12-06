from flask_restful import Resource

from kvc.daos.HemsireGozlemDAO import HemsireGozlemDAO

class IslemResource(Resource):
    """
    Hemsire Gozlem nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    hemsireGozlemDAO = HemsireGozlemDAO()

    def get(self, islem_id: int):
        """ islem_id parametresine karsılık Hemsire Gozlem bilgisi donen metod """

        hemsire_gozlem = self.hemsireGozlemDAO.find_by_id(islem_id)
        if not hemsire_gozlem:
            return {'message': 'Islem Not Found'}, 404
        return hemsire_gozlem.serialize, 200

    def delete(self, islem_id: int):
        """ islem_id parametresine göre Hemsire Gozlem nesnesini donen metod """

        hemsire_gozlem = self.hemsireGozlemDAO.find_by_id(islem_id)
        if not hemsire_gozlem:
            return {'message': 'Hemsire Gozlem Not Found'}, 404
        self.hemsireGozlemDAO.delete_from_db(hemsire_gozlem)
        return {'message': 'Hemsire Gozlem deleted.'}, 200
