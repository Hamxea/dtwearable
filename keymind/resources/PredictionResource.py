from flask_restful import Resource

from keymind.daos.PredictionDAO import PredictionDAO


class PredictionResource(Resource):
    """
    Prediction nesnesi için int tipinde id parametre alan metodları barındıran Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    predictionAlimiDAO = PredictionDAO()

    def get(self, prediction_id: int):
        """ prediction_id parametresine karsılık Prediction bilgisi donen metod """

        prediction = self.predictionAlimiDAO.find_by_id(prediction_id)
        if not prediction:
            return {'message': 'Prediction Not Found'}, 404
        return prediction.serialize, 200

    def delete(self, prediction_id: int):
        """ prediction_id parametresine karsılık gelen Prediction nesnesini veri tabanından silen metod """

        prediction = self.predictionAlimiDAO.find_by_id(prediction_id)
        if not prediction:
            return {'message': 'Prediction Not Found'}, 404
        self.predictionAlimiDAO.delete_from_db(prediction)
        return {'message': 'Prediction deleted.'}, 200