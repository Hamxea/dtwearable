from flask_restful import reqparse, Resource

from ai.restful.daos.NotificationDAO import NotificationDAO


class NotificationListResource(Resource):
    """ NotificationDTO nesnesi için islem_no'ya gore liste dönen metod """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('islem_no_list', type=int, required=True, action='append')

    dao = NotificationDAO()

    def get(self):
        """ Restful isteğinin body kısmında bulunan veriye gore NotificationDTO nesnesini liste olarak donmek icin kullanan metod """

        data = self.post_parser.parse_args()

        try:
            list = self.dao.get_by_islem_no(data['islem_no_list'])
            return list, 200
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while getting the item list. ",
                    "exception": str(e)
                    }, 500
