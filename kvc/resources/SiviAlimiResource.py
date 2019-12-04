from flask_restful import Resource

from kvc.daos.SiviAlimiDAO import SiviAlimiDAO


class SiviAlimiResource(Resource):
    siviAlimiDAO = SiviAlimiDAO()

    # @marshal_with(IslemRegisterResource.resource_fields)
    def get(self, sivi_alimi_id: int):
        sivi_alimi = self.siviAlimiDAO.find_by_id(sivi_alimi_id)
        if not sivi_alimi:
            return {'message': 'Sıvı Alımı Not Found'}, 404
        return sivi_alimi.serialize, 200

    def delete(self, sivi_alimi_id: int):
        sivi_alimi = self.siviAlimiDAO.find_by_id(sivi_alimi_id)
        if not sivi_alimi:
            return {'message': 'Sıvı Alımı Not Found'}, 404
        self.siviAlimiDAO.delete_from_db(sivi_alimi)
        return {'message': 'Sıvı Alımı deleted.'}, 200