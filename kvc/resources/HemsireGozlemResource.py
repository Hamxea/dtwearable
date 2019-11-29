from flask_restful import Resource

from kvc.daos.HemsireGozlemDAO import HemsireGozlemDAO


class HemsireGozlemResource(Resource):
    hemsireGozlemDAO = HemsireGozlemDAO()

    def get(self, hemsire_gozlem_id: int):
        hemsireGozlem = self.hemsireGozlemDAO.find_by_id(hemsire_gozlem_id)
        if not hemsireGozlem:
            return {'message': 'HemsireGozlem Not Found'}, 404
        return hemsireGozlem.serialize, 200

    def delete(self, hemsire_gozlem_id: int):
        hemsireGozlem = self.hemsireGozlemDAO.find_by_id(hemsire_gozlem_id)
        if not hemsireGozlem:
            return {'message': 'HemsireGozlem Not Found'}, 404
        self.hemsireGozlemDAO.delete_from_db(hemsireGozlem)
        return {'message': 'HemsireGozlem deleted.'}, 200
