import json
from datetime import datetime

from flask_restful import reqparse, Resource

from ai.restful.daos.AIModelDAO import AIModelDAO
from ai.restful.models.AIModel import AIModel
from ai.restful.services.AIModelTrainerService import AIModelTrainerService


class AIModelTrainerResource(Resource):
    """
    AI Modellerinin eğitilmesi için restful servisleri bulunduran metod
    """

    parser = reqparse.RequestParser()
    parser.add_argument('class_name', type=str, required=True)
    parser.add_argument('dataset_parameters', type=dict, required=True)
    parser.add_argument('hyperparameters', type=dict, required=True)

    ai_model_trainer_service = AIModelTrainerService()
    ai_model_dao = AIModelDAO()

    def post(self):
        """
        Sınıf adı gönderilen ai model nesnesinden model üreten
        Diske yazan
        Veritabanı kaydını yemni versiyon numarası ile oluşturan restful servisi
        """

        data = self.parser.parse_args()
        last_model = self.ai_model_dao.find_last_enabled_version_by_name(data['class_name'])

        ai_model_file_name, performance_metrics = self.ai_model_trainer_service.train(data['class_name'], data['dataset_parameters'], data['hyperparameters'])
        # TODO exception oluşması durumuna karşı önlem alınmalı

        ai_model = AIModel(id=None,
                           class_name=data['class_name'],
                           version=1 if last_model is None else last_model.version + 1,
                           model_url=ai_model_file_name,
                           parameters=json.dumps({'dataset_parameters': data['dataset_parameters'], 'hyperparameters': data['hyperparameters']}),
                           performance_metrics=json.dumps(performance_metrics),
                           enabled=False,
                           date_created=datetime.now())
        self.ai_model_dao.save_to_db(ai_model)
        return ai_model.serialize, 201
