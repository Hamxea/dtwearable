import json
import pickle
from datetime import datetime

from ai.restful.daos.AIModelDAO import AIModelDAO
from ai.restful.daos.PredictionDAO import PredictionDAO
from ai.restful.models.PredictionDTO import PredictionDTO


class PredictionService():
    """ Predict sınıfını kullanarak üretilen tahminlerin veri tabanına kaydının yapıldığı sınıf """

    ai_model_dao = AIModelDAO()
    prediction_dao = PredictionDAO()

    def myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def make_prediction(self, ai_model_class, reference_table, reference_id, prediction_input):
        """ Yapay zeka modeli, ilgili referans tablosu, referans id'si ve tahmin girdisini kullanarak tahmin üreten metod
            Tahmin sonrası prediction_dto veri tabanına kayıt edilir
            prediction_dto objesi return edilir
        """

        ai_model_dto = self.ai_model_dao.find_last_enabled_version_by_name(ai_model_class)
        model = self.load_model(ai_model_dto.model_url)

        prediction_input = [value[1:] for value in prediction_input]
        prediction_dto = PredictionDTO(id=None, reference_table=reference_table, reference_id=reference_id,
                                       prediction_input=json.dumps(prediction_input),
                                       prediction_value=None,
                                       prediction_error=None, prediction_date=datetime.now(),
                                       ai_model_id=ai_model_dto.id)

        try:
            if ai_model_class == "ai.aimodels.GenelTestPredict.GenelTestPredict":
                """Genel agoritma ile genel tahminin"""
                # do something
                new_prediction = self._predict_genel(model, prediction_input)
                new_prediction_dto_kural = new_prediction

                for pred_range in range(len(new_prediction.tolist()[0])):
                    prediction_dto.prediction_value = new_prediction.tolist()[0][pred_range]
                    self.prediction_dao.save_to_db(prediction_dto)
                prediction_dto.prediction_value = new_prediction_dto_kural
                return prediction_dto
            else:
                """ tek özellik tahmini için"""
                from sklearn.preprocessing import MinMaxScaler
                import numpy as np

                scaler = MinMaxScaler(feature_range=(0, 1))

                # prediction_input  = [value[1] for value in prediction_input]
                # prediction_input['ates']
                # scaler.fit_transform(np.array(prediction_input[0]).reshape(-1, 1))
                prediction_input = np.array(prediction_input).reshape(1, -1)

                # new_prediction = self._predict(model, prediction_input)
                new_prediction = self._predict_tek(model, prediction_input)
                prediction_dto.prediction_value = new_prediction[0]
                self.prediction_dao.save_to_db(prediction_dto)
                return prediction_dto

        except Exception as e:
            prediction_dto.prediction_error = str(e)
            self.prediction_dao.save_to_db(prediction_dto)
            raise Exception("Error occured while predicting")

    def _predict(self, model, prediction_input):
        """
        Modeli kullanarak tahmin yapan metod
        """

        """
        Örnek input formatı
        {
         "ates": [35, 36],
         "nabız": [100, 120]
        }
        veya
        {
            "ates": [35, 36]
        }
        """

        input = []
        for key in prediction_input:
            input.append(prediction_input[key])

        return model._predict(input)

    def _predict_tek(self, model, prediction_input):
        return model.predict(prediction_input)

    def _predict_genel(self, model, prediction_input):
        return model.forecast(prediction_input, steps=1)

    def load_model(self, model_url):
        """ Modeli dosya sisteminden yükleyen metod """

        return pickle.load(open(model_url, 'rb'))
