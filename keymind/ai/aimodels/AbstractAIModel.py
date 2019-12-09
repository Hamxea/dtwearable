from abc import ABC, abstractmethod


class AbstractAIModel(ABC):

    @abstractmethod
    def train(self, dataset_parameters, hyperparameters): pass