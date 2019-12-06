from datetime import datetime

from flask_restful import reqparse, Resource

from keymind.daos.PredictionDAO import PredictionDAO
from keymind.models.Prediction import Prediction


class PredictionRegisterResource(Resource):
    """
    Prediction nesnesi için parametre almayan metodları barındıran Register Resource sınıfı
    Restful istek tiplerine karşılık metodlar oluşturulur
    """

    prediction_post_parser = reqparse.RequestParser()
    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """

    prediction_post_parser.add_argument('id',
                                        type=int,
                                        required=False,
                                        )
    prediction_post_parser.add_argument('islem_id',
                                        type=int,
                                        required=True,
                                        )
    prediction_post_parser.add_argument('prediction_value',
                                        type=int,
                                        required=True,
                                        )
    prediction_post_parser.add_argument('prediction_date',
                                        type=lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date(),
                                        required=True,
                                        )
    prediction_post_parser.add_argument('ai_model_id',
                                        type=int,
                                        required=True
                                        )

    predictionDAO = PredictionDAO()

    def post(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Prediction nesnesini olusturan ve veritabanına yazan metod """

        data = self.prediction_post_parser.parse_args()

        prediction = Prediction(**data)

        try:
            self.predictionDAO.save_to_db(prediction)
        except Exception as e:
            return {"message": "An error occurred while inserting the item. ",
                    "exception": e
                    }, 500

        return prediction.serialize, 201

    def put(self):
        """ Restful isteğinin body kısmında bulunan veriye gore Islem nesnesini olusturan veya guncelleyen metod """

        data = self.prediction_post_parser.parse_args()

        prediction = self.predictionDAO.find_by_id(data['id'])

        if prediction:
            prediction.islem_id = data['islem_id']
            prediction.prediction_value = data['prediction_value']
            prediction.prediction_date = data['prediction_date']
            prediction.ai_model_id = data['ai_model_id']
        else:
            prediction = Prediction(**data)

        self.predictionDAO.save_to_db(prediction)

        return prediction.serialize