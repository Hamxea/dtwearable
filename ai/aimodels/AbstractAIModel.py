from abc import ABC, abstractmethod
from datetime import datetime


class AbstractAIModel(ABC):
    """ AI Model sınıflarının üst sınıfı olarak kullanılan Abstract sınıf """

    @abstractmethod
    def train(self, dataset_parameters, hyperparameters):
        """ Model'in eğitim için kullandığı train metodu, dataset ve hyper parametre detayları alır """

        pass

    @abstractmethod
    def get_statistics(self, start_date: datetime, end_date: datetime):
        """ Belirli tarih aralığındaki model istatistiklerini getirmek için kullanılan metot """

        pass