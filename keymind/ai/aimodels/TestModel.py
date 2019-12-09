from keymind.ai.aimodels.AbstractAIModel import AbstractAIModel


class TestModel():

    def train(self, dataset_parameters, hyperparameters):
        print("train()")
        print("dataset_parameters", dataset_parameters)
        print("hyperparameters", hyperparameters)

        return {"key": "value"}
