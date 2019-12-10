from abc import ABC, abstractmethod


class AbstractAIModel(ABC):
    """ AI Model sınıflarının üst sınıfı olarak kullanılan Abstract sınıf """

    @abstractmethod
    def train(self, dataset_parameters, hyperparameters):
        """ Model'in eğitim için kullandığı train metodu, dataset ve hyper parametre detayları alır """

        pass