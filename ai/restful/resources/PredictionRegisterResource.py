import logging

from flask_restful import reqparse, Resource

from ai.restful.services.PredictionService import PredictionService


class PredictionRegisterResource(Resource):
    """
    Prediction nesnesi için parametre almayan metodları barındıran Register Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    prediction_post_parser = reqparse.RequestParser()
    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """

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
        """ Restful isteğinin body kısmında bulunan veriye gore Prediction nesnesini olusturan ve veritabanına yazan metod """

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

