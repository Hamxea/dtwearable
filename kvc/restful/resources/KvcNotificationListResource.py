from flask_restful import reqparse, Resource

from kvc.restful.daos.KvcNotificationDAO import KvcNotificationDAO


class KvcNotificationRegisterResource(Resource):
    """ KvcNotificationDTO nesnesi için islem_no'ya gore liste dönen metod """

    """ Restful isteklerini tanımlamak icin olusturulur, uyumsuzluk halinde hata donmesi saglanır """
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('islem_no_list', type=list, required=True)

    dao = KvcNotificationDAO()

    def get(self):
        """ Restful isteğinin body kısmında bulunan veriye gore KvcNotificationDTO nesnesini liste olarak donmek icin kullanan metod """

        data = self.post_parser.parse_args()

        try:
            list = self.dao.get_by_islem_no(data['islem_no_list'])
            return list, 200
        except Exception as e:
            print(str(e))
            return {"message": "An error occurred while inserting the item. ",
                    "exception": str(e)
                    }, 500
