from flask_restful import Resource

from kvc.restful.daos.SiviAlimiDAO import SiviAlimiDAO


class SiviAlimiResource(Resource):
    """
    Sıvı Alımı nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    siviAlimiDAO = SiviAlimiDAO()

    def get(self, sivi_alimi_id: int):
        """ sivi_alimi_id parametresine karsılık Sıvı Alımı bilgisi donen metod """

        sivi_alimi = self.siviAlimiDAO.find_by_id(sivi_alimi_id)
        if not sivi_alimi:
            return {'message': 'Sıvı Alımı Not Found'}, 404
        return sivi_alimi.serialize, 200

    def delete(self, sivi_alimi_id: int):
        """ sivi_alimi_id parametresine karsılık gelen Sıvı Alımı nesnesini veri tabanından silen metod """

        sivi_alimi = self.siviAlimiDAO.find_by_id(sivi_alimi_id)
        if not sivi_alimi:
            return {'message': 'Sıvı Alımı Not Found'}, 404
        self.siviAlimiDAO.delete_from_db(sivi_alimi)
        return {'message': 'Sıvı Alımı deleted.'}, 200