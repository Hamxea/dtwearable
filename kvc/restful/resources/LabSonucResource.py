from flask_restful import Resource

from kvc.restful.daos.LabSonucDAO import LabSonucDAO


class LabSonucResource(Resource):
    """
    LabSonuc nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    dao = LabSonucDAO()

    def get(self, lab_sonuc_id: int):
        """ _id parametresine karsılık LabSonuc bilgisi donen metod """

        dto = self.dao.find_by_id(lab_sonuc_id)
        if not dto:
            return {'message': 'Object Not Found'}, 404
        return dto.serialize, 200

    def delete(self, lab_sonuc_id: int):
        """ _id parametresine göre LabSonuc nesnesini silen metod """

        dto = self.dao.find_by_id(lab_sonuc_id)
        if not dto:
            return {'message': 'Object Not Found'}, 404
        self.dao.delete_from_db(dto)
        return {'message': 'Object deleted.'}, 200
