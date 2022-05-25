from flask_restful import reqparse, Resource

from ai.restful.daos.NotificationDAO import NotificationDAO


class NotificationListResource(Resource):
    """ Method that returns list according to action_id for NotificationDTO object """

    """ created to define Restful requests, error returns in case of incompatibility. """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('islem_no_list', type=int, required=True, action='append')

    dao = NotificationDAO()

    def get(self):
        """ Method that uses the NotificationDTO object to return a list according
         to the data in the body of the Restful request """

        data = self.post_parser.parse_args()

        try:
            list = self.dao.get_by_islem_no(data['islem_no_list'])
            return list, 200
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while getting the item list. ",
                    "exception": str(e)
                    }, 500
