from datetime import datetime

from flask_restful import reqparse, Resource

from ai.restful.services.StatisticsService import StatisticsService


class StatisticsResource(Resource):
    """ İstatistik hesaplamaları için kullanılacak resource """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('start_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y").date(), required=True)
    post_parser.add_argument('end_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y").date(), required=True)

    def post(self):
        """ Restful isteğinin body kısmında bulunan tarih aralığına göre tahmin sayısı ve doğru tahmin sayısını return
            eden get_statistics metodunu çağıran metot
        """

        data = self.post_parser.parse_args()
        statistics = StatisticsService()
        try:
            return statistics.get_statistics(data['start_date'], data['end_date']), 201
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while querying. ",
                    "exception": str(e)
                    }, 500
