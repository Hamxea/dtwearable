from flask_restful import Resource, reqparse


class AbstractUserResource(Resource):
    """ Abstract class containing common codes for User Resource classes """

    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('password',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('role',
                              type=int,
                              required=True,
                              help="This field cannot be blank."
                              )
