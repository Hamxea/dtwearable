from ai.aimodels.AbstractAIModel import AbstractAIModel
from ai.restful.daos.AIModelDAO import AIModelDAO
from ai.restful.services.AIModelTrainerService import AIModelTrainerService


class StatisticsService():
    """ Genel durum tahminleri için istatistiklerin hesaplandığı sınıf """

    ai_model_dao = AIModelDAO()

    def get_statistics(self,start_date, end_date):
        """ İlgili tarih aralığı için toplam tahmin sayısı ile doğru tahmin sayısını dönen metot """

        """ Veritabanında aktif olan ai_model sınıflarını al """
        list_of_models = self.ai_model_dao.get_enabled_models()

        statistics_dict = {}
        for model in list_of_models:

            try:
                """ Aktif model class_name'ini kullanarak instance oluştur """
                ai_model = AIModelTrainerService.get_class(model.class_name)()

                """ oluşan instance AbstractAIModel sınıfdan mı türetilmiş kontrol et """
                if not isinstance(ai_model, AbstractAIModel):
                    raise Exception("{} class is not instance of AbstractAIModel!!!".format(model.class_name))

                """ Her model için get_statistics() metodunu çağırarak dönen dict nesneyi birleştir """
                statistics_dict[model.class_name] = ai_model.get_statistics(start_date, end_date)
            except Exception as e:
                logging.exception(e, exc_info=True)

        return statistics_dict