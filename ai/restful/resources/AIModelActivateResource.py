from flask_restful import reqparse, Resource

from ai.restful.daos.AIModelDAO import AIModelDAO


class AIModelActivateResource(Resource):
    """
    Method with restful services for training AI Models
    """

    parser = reqparse.RequestParser()
    parser.add_argument('class_name', type=str, required=True)
    parser.add_argument('version', type=int, required=True)

    ai_model_dao = AIModelDAO()

    def put(self):
        """ Activates the ai_model object with its name and version values and disables other versions """

        data = self.parser.parse_args()
        try:
            self.ai_model_dao.activate_by_name_and_version(data['class_name'], data['version'])
            if data['version'] < 0:
                return {"message": "All AIModel items disabled!"}, 201
            return {"message": "AIModel activated name:{}, version:{}".format(data['class_name'], data['version'])}, 201
        except Exception as e:
            return {"message": "An error occurred while activating the item. ",
                    "exception": str(e)
                    }, 500
