from datetime import datetime

from flask_restful import reqparse, Resource

from ai.restful.services.StatisticsService import StatisticsService


class StatisticsResource(Resource):
    """ Resource to be used for statistical calculations """

    """ Created to define Restful requests, error returns in case of incompatibility. """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('start_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y").date(), required=True)
    post_parser.add_argument('end_date', type=lambda x: datetime.strptime(x, "%d.%m.%Y").date(), required=True)

    def post(self):
        """ Return the number of guesses and the number of correct guesses according to the date range found in the body of the Restful request
             The method that calls the get_statistics method
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
