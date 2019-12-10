from db import db
from ai.restful.daos.AbstractDAO import AbstractDAO
from ai.restful.models.AIModel import AIModel


class AIModelDAO(AbstractDAO):
    """
    AIModel nesnesi için veritabanı işlemlerinin yapıldığı metodları içerir
    """

    def find_by_id(self, _id: int) -> AIModel:
        """ _id değerine göre User nesnesini veritabanından getiren metod """

        return AIModel.query.filter_by(id=_id).first()

    def find_last_enabled_version_by_name(self, class_name: str) -> AIModel:
        """ AIModel tablosundan name  ve enabled = True olan en buyuk version sahibi  kaydı dönen metod """

        return AIModel.query.filter_by(class_name=class_name).order_by(AIModel.version.desc()).first()

    def find_by_name_and_enable(self, class_name: str) -> AIModel:
        """ AIModel tablosundan name  ve enabled = True olan kayıtların ilkini dönen metod """

        return AIModel.query.filter_by(class_name=class_name, enabled=True).first()

    def find_by_name_and_version(self, class_name: str, version: int) -> AIModel:
        """ AIModel tablosundan name  ve version değerlerine göre eşleşen kayıtların ilkini dönen metod """

        return AIModel.query.filter_by(class_name=class_name, version=version).first()

    def activate_by_name_and_version(self, class_name: str, version: int):
        """ AIModel tablosundan name'e ait kayıtlardan versiyon numarası dışındakileri pasif eden metod """

        if version >= 0:
            active_model = self.find_by_name_and_version(class_name, version)
            if active_model is None:
                raise Exception("AIModel not found by id and version!")

        AIModel.query.filter(AIModel.class_name == class_name, AIModel.version != version).update({AIModel.enabled: False}, synchronize_session=False)
        AIModel.query.filter(AIModel.class_name == class_name, AIModel.version == version).update({AIModel.enabled: True}, synchronize_session=False)
        db.session.commit()