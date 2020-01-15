from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa. statespace.varmax import VARMAX
import statsmodels.api as sm
from ai.aimodels.AbstractAIModel import AbstractAIModel


class VectorAutoregressionMovingAverage(AbstractAIModel):
    """ Vector Autoregression Moving-Average (VARMA) with 1-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        train_data, test_data = self.split_dataset(df, dataset_parameters['test_ratio'], hyperparameters['n_steps'])
        varma_model = self.train_varma(train_data, hyperparameters['n_steps'])
        score, acc = self.test_varma(varma_model, test_data)

        return varma_model, {"score": score, "accuracy": acc}

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
        #train_data = train_data.astype(int)
        #test_data = test_data.astype(int)

        return train_data, test_data

    def train_varma(self, train_data, n_steps):
        """ X_train ve y_train kullanarak varma modeli oluşturan metod """
        print(type(train_data))
        train_data = train_data.head(6)
        train_data = train_data.values.tolist()
        """
        train_data = train_data.loc[:, (train_data != train_data.iloc[0]).any()]
        train_data = train_data.values.tolist()
        print(type(train_data))
        """
        print(train_data)
        print(type(train_data))
        model = VARMAX(train_data, order=(1, 1, 1, 1, 1, 1))
        model_fit = model.fit(disp=False)
        return model_fit

    def test_varma(self, varma_model, test_data):
        """ Oluşturulmuş varma modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """

        #make prediction of test validation data
        prediction = varma_model.forecast()
        print(prediction)

        return 0, 1

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: Genel tahmin özeliklek kolumlar isimi yazilacak """
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
