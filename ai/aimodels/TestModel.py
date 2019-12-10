from ai.aimodels import AbstractAIModel


class TestModel(AbstractAIModel):
    """ AI Model algoritmalarını test etmek için oluşturulan test sınıfı """

    def train(self, dataset_parameters, hyperparameters):
        """ Test amaçlı boşcevap dönen metod """

        print("train()")
        print("dataset_parameters", dataset_parameters)
        print("hyperparameters", hyperparameters)

        return {"key": "value"}
