import json
from datetime import datetime

from flask_restful import reqparse, Resource

from ai.restful.daos.AIModelDAO import AIModelDAO
from ai.restful.models.AIModelDTO import AIModelDTO
from ai.restful.services.AIModelTrainerService import AIModelTrainerService


class AIModelTrainerResource(Resource):
    """
    Method with restful services for training AI Models
    """

    parser = reqparse.RequestParser()
    parser.add_argument('class_name', type=str, required=True)
    parser.add_argument('dataset_parameters', type=dict, required=True)
    parser.add_argument('hyperparameters', type=dict, required=True)

    ai_model_trainer_service = AIModelTrainerService()
    ai_model_dao = AIModelDAO()

    def post(self):
        """
         Generating model from ai model object whose class name is sent
         writes to disc
         Restful service that creates database record with new version number
        """

        data = self.parser.parse_args()
        last_model = self.ai_model_dao.find_last_enabled_version_by_name(data['class_name'])

        ai_model_file_name, performance_metrics = self.ai_model_trainer_service.train(data['class_name'], data['dataset_parameters'], data['hyperparameters'])
        # TODO add exception

        ai_model = AIModelDTO(id=None,
                              class_name=data['class_name'],
                              version=1 if last_model is None else last_model.version + 1,
                              model_url=ai_model_file_name,
                              parameters=json.dumps({'dataset_parameters': data['dataset_parameters'], 'hyperparameters': data['hyperparameters']}),
                              performance_metrics=json.dumps(performance_metrics),
                              enabled=False,
                              date_created=datetime.now())
        self.ai_model_dao.save_to_db(ai_model)
        return ai_model.serialize, 201
