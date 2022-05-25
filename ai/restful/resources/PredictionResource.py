from flask_restful import Resource

from ai.restful.daos.PredictionDAO import PredictionDAO


class PredictionResource(Resource):
    """
    Resource class that contains methods that take int type id parameter for Prediction object
     Methods are created to respond to Restful request types
    """

    predictionAlimiDAO = PredictionDAO()

    def get(self, prediction_id: int):
        """ Method that returns Prediction information corresponding to prediction id parameter """

        prediction = self.predictionAlimiDAO.find_by_id(prediction_id)
        if not prediction:
            return {'message': 'Prediction Not Found'}, 404
        return prediction.serialize, 200

    def delete(self, prediction_id: int):
        """ Method that deletes the Prediction object corresponding to the prediction id parameter from the database """

        # TODO This operation requires admin privileges

        prediction = self.predictionAlimiDAO.find_by_id(prediction_id)
        if not prediction:
            return {'message': 'Prediction Not Found'}, 404
        self.predictionAlimiDAO.delete_from_db(prediction)
        return {'message': 'Prediction deleted.'}, 200