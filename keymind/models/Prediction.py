import datetime
from builtins import float

from db import db


class Prediction(db.Model):
    """ Prediction tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = 'prediction'

    id = db.Column(db.BigInteger, primary_key=True)
    islem_id = db.Column(db.BigInteger)
    prediction_value = db.Column(db.Float)
    prediction_date = db.Column(db.DateTime)
    ai_model_id = db.Column(db.BigInteger)

    def __init__(self, id:int, islem_id: int, prediction_value: float, prediction_date: datetime, ai_model_id: int):

        self.id = id
        self.islem_id = islem_id
        self.prediction_value = prediction_value
        self.prediction_date = prediction_date
        self.ai_model_id = ai_model_id

    @property
    def serialize(self):
        """ Nesneyi json'a çeviren metod """

        return {
            'id': self.id,
            'islem_id': self.islem_id,
            'prediction_value': self.prediction_value,
            'prediction_date': self.prediction_date.strftime('%d.%m.%Y %H:%M:%S'),
            'ai_model_id': self.ai_model_id
        }
