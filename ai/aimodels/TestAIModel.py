from datetime import datetime

from sqlalchemy import text

from ai.aimodels.AbstractAIModel import AbstractAIModel
from db import db


class TestAIModel(AbstractAIModel):
    """ Hastanın genel durumu için tahmin yapan yapay zeka modeli """

    def train(self, dataset_parameters, hyperparameters):
        """ Test amaçlı boşcevap dönen metod """

        print("train()")
        print("dataset_parameters", dataset_parameters)
        print("hyperparameters", hyperparameters)

        return {"key": "value"}

    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Kategorik tahmin yapan yapay zeka modelleri için örnek istatistik sonucu """

        return {
            "total_prediction_count": 34,
            "performance_percentage": 67,
            "class_categories": [
                {
                    "class_name": "Taburcu",
                    "prediction_count": 12,
                    "number_of_correct_prediction": 11
                },
                {
                    "class_name": "Ameliyat",
                    "prediction_count": 23,
                    "number_of_correct_prediction": 12
                }
            ]
        }