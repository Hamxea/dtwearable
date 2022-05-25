import logging

from db import db


class AbstractDAO:
    """
    Abstract class of DAO objects on which database operations are performed
    Common database operations are defined in this method
    """

    pattern = None

    def __init__(self, model):
        self.model = model

    def save_to_db(self, model):
        """ Method that saves the model object in the database or updates it if it has an id """
        try:
            db.session.add(model)
            db.session.commit()
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Couldn't save into database! Object name is '{}'".format(type(model).__name__))

    def find_by_id(self, _id: int):
        """ Method fetching LabResult object from database based on _id value """

        try:
            return self.model.query.filter_by(id=_id).first()
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Couldn't find in database! Id is '{}'".format(id))

    def delete_from_db(self, model):
        """ Method to delete model object from database """
        try:
            db.session.delete(model)
            db.session.commit()
        except Exception as e:
            logging.exception(e, exc_info=True)
            raise Exception("Couldn't delete from database! Object name is '{}'".format(type(model).__name__))