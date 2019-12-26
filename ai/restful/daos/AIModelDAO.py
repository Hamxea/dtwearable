from sqlalchemy import text

from db import db
from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.AIModelDTO import AIModelDTO


class AIModelDAO(AbstractDAO):
    """
    AIModel nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def __init__(self):
        super().__init__(AIModelDTO)

    def get_enabled_models(self):
        """ AI_model tablosundaki enabled=true olan tüm kayıtları getiren metot"""

        return AIModelDTO.query.filter_by(enabled=True).all()

    def find_last_enabled_version_by_name(self, class_name: str) -> AIModelDTO:
        """ AIModel tablosundan name  ve enabled = True olan en buyuk version sahibi  kaydı dönen metod """

        return AIModelDTO.query.filter_by(class_name=class_name, enabled=True).order_by(AIModelDTO.version.desc()).first()

    def find_by_name_and_enable(self, class_name: str) -> AIModelDTO:
        """ AIModel tablosundan name  ve enabled = True olan kayıtların ilkini dönen metod """

        return AIModelDTO.query.filter_by(class_name=class_name, enabled=True).first()

    def find_by_name_and_version(self, class_name: str, version: int) -> AIModelDTO:
        """ AIModel tablosundan name  ve version değerlerine göre eşleşen kayıtların ilkini dönen metod """

        return AIModelDTO.query.filter_by(class_name=class_name, version=version).first()

    def activate_by_name_and_version(self, class_name: str, version: int):
        """ AIModel tablosundan name'e ait kayıtlardan versiyon numarası dışındakileri pasif eden metod """

        if version >= 0:
            active_model = self.find_by_name_and_version(class_name, version)
            if active_model is None:
                raise Exception("AIModel not found by id and version!")

        AIModelDTO.query.filter(AIModelDTO.class_name == class_name, AIModelDTO.version != version).update({AIModelDTO.enabled: False}, synchronize_session=False)
        AIModelDTO.query.filter(AIModelDTO.class_name == class_name, AIModelDTO.version == version).update({AIModelDTO.enabled: True}, synchronize_session=False)
        db.session.commit()