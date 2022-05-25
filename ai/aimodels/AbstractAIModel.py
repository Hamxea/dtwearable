from abc import ABC, abstractmethod
from datetime import datetime


class AbstractAIModel(ABC):
    """ Abstract class used as superclass of AI Model classes """

    @abstractmethod
    def train(self, dataset_parameters, hyperparameters):
        """ Gets the train method, dataset and hyper parameter details that the model uses for training """

        pass

    @abstractmethod
    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Abstract method used to fetch the model's statistics for a specific date range """

        pass