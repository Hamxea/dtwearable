import logging

from flask_restful import reqparse, Resource

from ai.restful.services.PredictionService import PredictionService


class PredictionRegisterResource(Resource):
    """
    Register Resource class that hosts methods that do not take parameters for the Prediction object
     Methods are created to respond to Restful request types
    """

    prediction_post_parser = reqparse.RequestParser()
    """ It is created to define Restful requests, error returns in case of incompatibility. """

    prediction_post_parser.add_argument('ai_model_class',
                                        type=str,
                                        required=True
                                        )
    prediction_post_parser.add_argument('reference_table',
                                        type=str,
                                        required=True,
                                        )
    prediction_post_parser.add_argument('reference_id',
                                        type=int,
                                        required=True,
                                        )
    prediction_post_parser.add_argument('prediction_input',
                                        type=dict,
                                        required=True,
                                        )

    predictionService = PredictionService()

    def post(self):
        """ The method that creates the Prediction object according to the data in the body of the Restful request and writes it to the database """

        data = self.prediction_post_parser.parse_args()

        try:
            prediction_dto = self.predictionService.make_prediction(data['ai_model_class'],
                                                   data['reference_table'],
                                                   data['reference_id'],
                                                   data['prediction_input'])
        except Exception as e:
            logging.exception(e, exc_info=True)
            return {"message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                    }, 500

        return prediction_dto.serialize, 201

