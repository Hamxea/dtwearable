import datetime
from builtins import float

from db import db


class PredictionDTO(db.Model):
    """ Prediction tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı """

    __tablename__ = 'prediction'

    id = db.Column(db.BigInteger, primary_key=True)
    reference_table = db.Column(db.String(64), nullable=False)
    reference_id = db.Column(db.BigInteger, nullable=False)
    prediction_input = db.Column(db.String(512), nullable=False)
    prediction_value = db.Column(db.String(512), nullable=False)
    prediction_error = db.Column(db.String(512))
    prediction_date = db.Column(db.DateTime, nullable=False)
    ai_model_id = db.Column(db.BigInteger, nullable=False)

    def __init__(self, id:int, reference_table: str, reference_id: int, prediction_input: str, prediction_value: str,
                 prediction_error:str, prediction_date: datetime, ai_model_id: int):

        self.id = id
        self.reference_table = reference_table
        self.reference_id = reference_id
        self.prediction_input = prediction_input
        self.prediction_value = prediction_value
        self.prediction_error = prediction_error
        self.prediction_date = prediction_date
        self.ai_model_id = ai_model_id

    @property
    def serialize(self):
        """ Nesneyi json'a çeviren metod """

        return {
            'id': self.id,
            'reference_table': self.reference_table,
            'reference_id': self.reference_id,
            'prediction_input': self.prediction_input,
            'prediction_value': self.prediction_value,
            'prediction_error': self.prediction_error,
            'prediction_date': self.prediction_date.strftime('%d.%m.%Y %H:%M:%S'),
            'ai_model_id': self.ai_model_id
        }
