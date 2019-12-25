from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split

from ai.aimodels.AbstractAIModel import AbstractAIModel


class VectorAutoRegression(AbstractAIModel):
    """ Tek değişkenli modeller için SVR kullanarak zaman serisi oluşturma modeli """

    window_size = None

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        df = self.windowing(df)
        train, valid = self.split_dataset(df, dataset_parameters['test_ratio'])

        svr_model = self.train_svr(train)

        score = self.test_svr(svr_model, valid)

        return svr_model, {"score": score}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        Dataset parametlerine göre train ve test'te kullanılacak dataseti getiren metod
        alt sınıflar tarafından implemente edilecektir
        """
        pass

    def create_synthetic_dataset(self):
        """ İhtiyaca göre sentetik olarak dataset oluşturan metod """

        df_size = 100
        low = 35
        high = 42

        df = DataFrame(np.random.uniform(low=low, high=high, size=df_size + self.window_size))
        df = round(df, 2)
        return df

    def windowing(self, df):
        """ tek boyutlu  veriyi window size'ı kullanarak matrise çeviren metod """

        agg_values = self.series_to_supervised(dataset=df, n_in=self.window_size)
        df = DataFrame(agg_values)
        self.rename_columns(df, 'Feat_')
        return df

    def split_dataset(self, data, test_ratio):
        """ Dataseti train ve test için bölen metod """

        """
        creating the train and validation set
        """
        train = data[:int(test_ratio * (len(data)))]
        valid = data[int(test_ratio * (len(data))):]

        return (valid, train)

    def train_svr(self, train):
        """ X_train ve y_train kullanarak SVR modeli oluşturan metod """

        from statsmodels.tsa.vector_ar.var_model import VAR

        model = VAR(endog=train)
        model_fit = model.fit()

        return model

    def test_svr(self, svr_model, valid):
        """ Oluşturulmuş SVR modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """

        model_fit = svr_model.fit()
        # make prediction on validation
        prediction = model_fit.forecast(model_fit.y, steps=len(valid))

        score = svr_model.score(valid)
        print("Score:", score)

        return score

    def series_to_supervised(self, dataset, n_in=3, n_out=1):
        """ Dataset formatını supervised öğrenme formatına çeviren metod """

        cols = list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(dataset.shift(i))
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(dataset.shift(-i))
        # put it all together
        agg = concat(cols, axis=1)
        # drop rows with NaN values
        agg.dropna(inplace=True)
        return agg.values


    def rename_columns(self, df, identifier='Feat_'):
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
