from flask_restful import Resource
from kvc.restful.daos.IslemOperasyonDAO import IslemOperasyonDAO

class IslemOperasyonResource(Resource):
    """
    Islem Operasyon nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    islemOperasyonDAO = IslemOperasyonDAO()

    def get(self, islem_operasyon_id: int):
        """ islem_operasyon_id parametresine karsılık Islem Operasyon bilgisi donen metod """

        islem_operasyon=self.islemOperasyonDAO.find_by_id(islem_operasyon_id)
        if not islem_operasyon:
            return {'message': 'Islem Operasyon Not Found'}, 404
        return islem_operasyon.serialize, 200

    def delete(self, islem_operasyon_id: int):
        """ islem_operasyon_id parametresine göre Islem Operasyon nesnesini donen metod """

        islem_operasyon = self.islemOperasyonDAO.find_by_id(islem_operasyon_id)
        if not islem_operasyon:
            return {'message': 'Islem Operasyon Not Found'}, 404
        self.islemOperasyonDAO.delete_from_db(islem_operasyon)
        return {'message': 'Islem Operasyon deleted.'}, 200