from flask_restful import Resource

from kvc.daos.IslemDAO import IslemDAO


class IslemResource(Resource):
    islemDAO = IslemDAO()

    # @marshal_with(IslemRegisterResource.resource_fields)
    def get(self, islem_id: int):
        islem = self.islemDAO.find_by_id(islem_id)
        if not islem:
            return {'message': 'Islem Not Found'}, 404
        return islem.serialize, 200

    def delete(self, islem_id: int):
        islem = self.islemDAO.find_by_id(islem_id)
        if not islem:
            return {'message': 'Islem Not Found'}, 404
        self.islemDAO.delete_from_db(islem)
        return {'message': 'Islem deleted.'}, 200