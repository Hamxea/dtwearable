from flask_restful import Resource

from kvc.daos.IslemDAO import IslemDAO

"""
Islem nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
Restful istek tiplerine karşılık metodlar oluşturulur
"""
class IslemResource(Resource):
    islemDAO = IslemDAO()

    # islem_id parametresine karsılık Islem bilgisi donen metod
    def get(self, islem_id: int):
        islem = self.islemDAO.find_by_id(islem_id)
        if not islem:
            return {'message': 'Islem Not Found'}, 404
        return islem.serialize, 200

    # islem_id parametresine göre Islem nesnesini donen metod
    def delete(self, islem_id: int):
        islem = self.islemDAO.find_by_id(islem_id)
        if not islem:
            return {'message': 'Islem Not Found'}, 404
        self.islemDAO.delete_from_db(islem)
        return {'message': 'Islem deleted.'}, 200