from sqlalchemy import text

from db import db
from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.AIModelDTO import AIModelDTO


class AIModelDAO(AbstractDAO):
    """
    Contains methods by which database operations are performed for the AIModel object
    """

    def __init__(self):
        super().__init__(AIModelDTO)

    def get_enabled_models(self):
        """ Method to retrieve all records with enabled=true in AI_model table"""

        return AIModelDTO.query.filter_by(enabled=True).all()

    def find_last_enabled_version_by_name(self, class_name: str) -> AIModelDTO:
        """ Method that returns the largest version owner record with name and enabled = True from the AIModel table """

        return AIModelDTO.query.filter_by(class_name=class_name, enabled=True).order_by(AIModelDTO.version.desc()).first()

    def find_by_name_and_enable(self, class_name: str) -> AIModelDTO:
        """ Method that returns the first of the records with name and enabled = True from the AIModel table """

        return AIModelDTO.query.filter_by(class_name=class_name, enabled=True).first()

    def find_by_name_and_version(self, class_name: str, version: int) -> AIModelDTO:
        """ The method that returns the first of the matching records from the AIModel table by name and version values ​​"""

        return AIModelDTO.query.filter_by(class_name=class_name, version=version).first()

    def activate_by_name_and_version(self, class_name: str, version: int):
        """ Method that disables records of name from AIModel table except version number """

        if version >= 0:
            active_model = self.find_by_name_and_version(class_name, version)
            if active_model is None:
                raise Exception("AIModel not found by id and version!")

        AIModelDTO.query.filter(AIModelDTO.class_name == class_name, AIModelDTO.version != version).update({AIModelDTO.enabled: False}, synchronize_session=False)
        AIModelDTO.query.filter(AIModelDTO.class_name == class_name, AIModelDTO.version == version).update({AIModelDTO.enabled: True}, synchronize_session=False)
        db.session.commit()