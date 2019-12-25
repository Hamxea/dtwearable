from datetime import datetime

from sqlalchemy import text

from ai.aimodels.AbstractAIModel import AbstractAIModel
from db import db


class PatientStatusPredictionAIModel(AbstractAIModel):
    """ Hastanın genel durumu için tahmin yapan yapay zeka modeli """

    def train(self, dataset_parameters, hyperparameters):
        """ Model'in eğitim için kullandığı train metodu, dataset ve hyper parametre detayları alır """

        pass

    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Modelin belirli tarih aralığındaki istatistiklerini getirmek için kullanılan metot """

        formatted_start_date = start_date.strftime('%d.%m.%Y')
        formatted_end_date = end_date.strftime('%d.%m.%Y')

        sql_text = text("select count(*), sum(case when p.prediction_value = i.etiket then 1 else 0 end) true_count "
                        "from prediction p, islem i, ai_model ai where p.reference_table = 'islem' and p.reference_id = i.islem_no "
                        "and ai.class_name = 'ai.aimodels.PatientStatusPredictionAIModel.PatientStatusPredictionAIModel' "
                        "and p.ai_model_id = ai.id and p.prediction_date > TO_DATE(:start_date, 'DD.MM.YYYY')"
                        "and p.prediction_date < TO_DATE(:end_date, 'DD.MM.YYYY')")

        # TODO : Genel durum kategorilerine (labellar) göre istatistiklerin detaylandırılması
        # Label'lar bir döngüye alınarak, her bir label için sorguya and koşulu eklenmeli
        # Her label için istatistik sonuçları hesaplanıp, json'a eklenmeli
        # Örnek json TestAIModel.py sınıfında yer almaktadır

        result = db.session.execute(sql_text,
                                    {'start_date': formatted_start_date, 'end_date': formatted_end_date}).fetchall()

        total_count = result[0][0]
        true_count = result[0][1]

        if true_count is None:
            return {"true_count": None}
        else:
            return {'total_count': total_count,
                    'true_count': true_count}