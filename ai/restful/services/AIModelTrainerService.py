import os
import pickle
from datetime import datetime
from pathlib import Path

from ai.aimodels.AbstractAIModel import AbstractAIModel


class AIModelTrainerService:
    """ """

    # User home altında ai_models klasörünün path'i
    file_path = str(Path.home()) + "\\ai_models"

    def __init__(self):
        # Eğer file_path klasörü dosya sisteminde yoksa oluştur
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def train(self, ai_model_class: str, dataset_parameters, hyper_parameters):
        """ Model sınıfı kullanılarak model dosyası oluşturulur ve kaydedilir"""

        ai_model = AIModelTrainerService.get_class(ai_model_class)()
        if not isinstance(ai_model, AbstractAIModel):
            raise Exception("{} class is not instance of AbstractAIModel!!!".format(ai_model_class))
        trained_model, performance_metrics = ai_model.train(dataset_parameters, hyper_parameters)
        ai_model_file_name = self.save_model(ai_model_class, trained_model)

        return ai_model_file_name, performance_metrics
        

    def save_model(self, ai_model_class, trained_model):
        """ Model dosyası pickle ile kaydediliyor """

        ai_model_file_name = self.file_path + "\\" + ai_model_class + "_" + str(datetime.now().timestamp()) + ".pickle"
        pickle.dump(trained_model, open(ai_model_file_name, 'wb'))
        print("ai_model_file_name:", ai_model_file_name)
        return ai_model_file_name

    @staticmethod
    def get_class(class_name):
        parts = class_name.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
