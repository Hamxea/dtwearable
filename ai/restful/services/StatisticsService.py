import logging

from ai.aimodels.AbstractAIModel import AbstractAIModel
from ai.restful.daos.AIModelDAO import AIModelDAO
from ai.restful.services.AIModelTrainerService import AIModelTrainerService


class StatisticsService():
    """ Class for which statistics are calculated for general condition forecasts """

    ai_model_dao = AIModelDAO()

    def get_statistics(self,start_date, end_date):
        """ Method that returns the total number of predictions and the number of correct predictions for the relevant date range """

        """ Get active ai_model classes in database """
        list_of_models = self.ai_model_dao.get_enabled_models()

        statistics_dict = {}
        for model in list_of_models:

            try:
                """ Create instance using active model class_name """
                ai_model = AIModelTrainerService.get_class(model.class_name)()

                """ Check if the resulting instance is derived from AbstractAIModel class """
                if not isinstance(ai_model, AbstractAIModel):
                    raise Exception("{} class is not instance of AbstractAIModel!!!".format(model.class_name))

                """ Merge the returned dict object by calling the get_statistics() method for each model """
                statistics_dict[model.class_name] = ai_model.get_statistics(start_date, end_date)
            except Exception as e:
                logging.exception(e, exc_info=True)

        return statistics_dict