from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split
from statsmodels.tsa.vector_ar.var_model import VAR

from ai.aimodels.AbstractAIModel import AbstractAIModel


class VectorAutoRegression(AbstractAIModel):
    """ Tek değişkenli modeller için VAR kullanarak zaman serisi oluşturma modeli """

    """ Mutlilayer (MLP) Perceptron with 1-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        train_data, test_data = self.split_dataset(df, dataset_parameters['test_ratio'], hyperparameters['n_steps'])
        mlp_model = self.train_mlp(train_data, hyperparameters['n_steps'])
        score, acc = self.test_mlp(mlp_model, test_data)

        return mlp_model, {"score": score, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        Dataset parametlerine göre train ve test'te kullanılacak dataseti getiren metod
        alt sınıflar tarafından implemente edilecektir
        """
        pass

    def split_dataset(self, df, test_ratio, n_Steps):
        """ Dataseti train ve test için bölen metod """

        train_data = df[:int((1-test_ratio)*len(df))]
        test_data = df[int((1-test_ratio)*len(df)):]

        return train_data, test_data

    def train_mlp(self, train_data, n_steps):
        """ X_train ve y_train kullanarak mlp modeli oluşturan metod """

        model = VAR(endog=train_data)
        model_fit = model.fit()
        return model_fit

    def test_mlp(self, mlp_model, test_data):
        """ Oluşturulmuş mlp modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """

        #make prediction of test validation data
        prediction = mlp_model.forcast(mlp_model.y, steps=len(test_data))
        print(prediction)

        return 0, 0

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: Genel tahmin özeliklek kolumlar isimi yazilacak """
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
